import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# ---------------- CONFIG ----------------
st.set_page_config(page_title="🏋️ Gym Workout Logger", layout="centered")

# ---------------- STATE ----------------
if "workouts" not in st.session_state:
    st.session_state.workouts = pd.DataFrame(
        columns=["Date", "Exercise", "Sets", "Reps", "Weight (kg)"]
    )
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None  # Track row being edited

# ---------------- INPUT FORM ----------------
st.title("🏋️ Gym Workout Logger")

# If editing, prefill with existing row
if st.session_state.edit_index is not None:
    row = st.session_state.workouts.loc[st.session_state.edit_index]
    default_date = pd.to_datetime(row["Date"]).date()
    default_exercise = row["Exercise"]
    default_sets = int(row["Sets"])
    default_reps = int(row["Reps"])
    default_weight = float(row["Weight (kg)"])
else:
    default_date = datetime.date.today()
    default_exercise = "Bicep Curl"
    default_sets = 3
    default_reps = 10
    default_weight = 20.0

# Date selector
date = st.date_input("Select Date", default_date)

# Exercise dropdown
exercise = st.selectbox(
    "Exercise Type",
    ["Bicep Curl", "Arms", "Shoulder", "Legs", "Triceps", "Core", "Chest", "Back"],
    index=(
        ["Bicep Curl", "Arms", "Shoulder", "Legs", "Triceps", "Core", "Chest", "Back"].index(default_exercise)
    ),
)

# Input for sets, reps, weight
col1, col2, col3 = st.columns(3)
with col1:
    sets = st.number_input("Sets", min_value=1, max_value=10, value=default_sets)
with col2:
    reps = st.number_input("Reps", min_value=1, max_value=50, value=default_reps)
with col3:
    weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, value=default_weight)

# Add or Update button
if st.session_state.edit_index is None:
    if st.button("➕ Add Exercise"):
        new_entry = pd.DataFrame(
            [[date, exercise, sets, reps, weight]],
            columns=["Date", "Exercise", "Sets", "Reps", "Weight (kg)"],
        )
        st.session_state.workouts = pd.concat(
            [st.session_state.workouts, new_entry], ignore_index=True
        )
        st.success("Workout added!")
else:
    if st.button("💾 Update Exercise"):
        st.session_state.workouts.loc[st.session_state.edit_index] = [date, exercise, sets, reps, weight]
        st.session_state.edit_index = None
        st.success("Workout updated!")

# ---------------- HISTORY TABLE ----------------
st.subheader("📋 Workout History")

if st.session_state.workouts.empty:
    st.info("No workout data yet.")
else:
    for idx, row in st.session_state.workouts.iterrows():
        cols = st.columns([2, 2, 1, 1, 1, 0.5, 0.5])  # layout for row + icons
        cols[0].write(pd.to_datetime(row["Date"]).date())
        cols[1].write(row["Exercise"])
        cols[2].write(int(row["Sets"]))
        cols[3].write(int(row["Reps"]))
        cols[4].write(float(row["Weight (kg)"]))
        edit_btn = cols[5].button("✏️", key=f"edit_{idx}")
        delete_btn = cols[6].button("🗑️", key=f"delete_{idx}")

        if edit_btn:
            st.session_state.edit_index = idx
            st.experimental_rerun()

        if delete_btn:
            st.session_state.workouts.drop(idx, inplace=True)
            st.session_state.workouts.reset_index(drop=True, inplace=True)
            st.success("Workout deleted!")
            st.experimental_rerun()

# ---------------- WEEKLY PROGRESS GRAPH ----------------
st.subheader("📊 Weekly Progress")

if not st.session_state.workouts.empty:
    df = st.session_state.workouts.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # ✅ Cutoff for last 7 days
    cutoff = pd.Timestamp(datetime.date.today() - datetime.timedelta(days=7))
    last_week = df[df["Date"] >= cutoff]

    if not last_week.empty:
        # Calculate total volume = sets × reps × weight
        last_week["Total Volume"] = (
            last_week["Sets"] * last_week["Reps"] * last_week["Weight (kg)"]
        )

        # ✅ Aggregate per day per exercise
        daily_exercise_totals = (
            last_week.groupby([last_week["Date"].dt.date, "Exercise"])["Total Volume"]
            .sum()
            .reset_index()
        )

        # ✅ Stacked bar chart
        fig = px.bar(
            daily_exercise_totals,
            x="Date",
            y="Total Volume",
            color="Exercise",
            title="Daily Workout Volume by Exercise (last 7 days)",
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No workouts logged in the last 7 days.")
