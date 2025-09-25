import streamlit as st
import random
import time

# Configure page
st.set_page_config(
    page_title="🎮 Rock Paper Scissors",
    page_icon="✂️",
    layout="centered"
)

# Custom CSS for styling and animations
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: pulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes pulse {
        from { transform: scale(1); }
        to { transform: scale(1.05); }
    }
    
    .game-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .score-board {
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .score-item {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .choice-button {
        font-size: 4rem;
        padding: 1rem;
        margin: 0.5rem;
        border: none;
        border-radius: 50%;
        background: linear-gradient(45deg, #48cae4, #0077b6);
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .choice-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .battle-area {
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
    }
    
    .choice-display {
        font-size: 6rem;
        margin: 1rem;
        display: inline-block;
        animation: bounce 0.6s ease;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(-10px); }
    }
    
    .result-text {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .win { color: #00ff88; }
    .lose { color: #ff6b6b; }
    .tie { color: #ffd700; }
    
    .stats-container {
        background: linear-gradient(45deg, #a8e6cf, #88d8c0);
        color: #2c3e50;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .reset-button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .reset-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #48cae4, #0077b6) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.ties = 0
    st.session_state.total_games = 0
    st.session_state.last_result = None
    st.session_state.player_choice = None
    st.session_state.computer_choice = None
    st.session_state.game_history = []

# Game choices
CHOICES = {
    'Rock': '🪨',
    'Paper': '📄', 
    'Scissors': '✂️'
}

def get_computer_choice():
    """Get random choice for computer"""
    return random.choice(list(CHOICES.keys()))

def determine_winner(player, computer):
    """Determine the winner of the round"""
    if player == computer:
        return "tie"
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Paper" and computer == "Rock") or \
         (player == "Scissors" and computer == "Paper"):
        return "win"
    else:
        return "lose"

def play_round(player_choice):
    """Play a single round"""
    computer_choice = get_computer_choice()
    result = determine_winner(player_choice, computer_choice)
    
    # Update session state
    st.session_state.player_choice = player_choice
    st.session_state.computer_choice = computer_choice
    st.session_state.last_result = result
    st.session_state.total_games += 1
    
    # Update scores
    if result == "win":
        st.session_state.player_score += 1
    elif result == "lose":
        st.session_state.computer_score += 1
    else:
        st.session_state.ties += 1
    
    # Add to history
    st.session_state.game_history.append({
        'round': st.session_state.total_games,
        'player': player_choice,
        'computer': computer_choice,
        'result': result
    })
    
    # Keep only last 10 games in history
    if len(st.session_state.game_history) > 10:
        st.session_state.game_history.pop(0)

def reset_game():
    """Reset all game statistics"""
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.ties = 0
    st.session_state.total_games = 0
    st.session_state.last_result = None
    st.session_state.player_choice = None
    st.session_state.computer_choice = None
    st.session_state.game_history = []

def get_win_percentage():
    """Calculate win percentage"""
    if st.session_state.total_games == 0:
        return 0
    return (st.session_state.player_score / st.session_state.total_games) * 100

# Main app layout
st.markdown('<h1 class="main-title">🎮 Rock Paper Scissors 🎮</h1>', unsafe_allow_html=True)

# Game container
st.markdown('<div class="game-container">', unsafe_allow_html=True)

# Score board
st.markdown(f"""
<div class="score-board">
    <div class="score-item">🏆 SCOREBOARD 🏆</div>
    <div class="score-item">You: {st.session_state.player_score} | Computer: {st.session_state.computer_score} | Ties: {st.session_state.ties}</div>
    <div class="score-item">Total Games: {st.session_state.total_games}</div>
</div>
""", unsafe_allow_html=True)

# Game controls
st.markdown("### 🎯 Choose Your Weapon!")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(f"{CHOICES['Rock']} Rock", key="rock", use_container_width=True):
        play_round("Rock")
        st.rerun()

with col2:
    if st.button(f"{CHOICES['Paper']} Paper", key="paper", use_container_width=True):
        play_round("Paper")
        st.rerun()

with col3:
    if st.button(f"{CHOICES['Scissors']} Scissors", key="scissors", use_container_width=True):
        play_round("Scissors")
        st.rerun()

# Battle area - show last round results
if st.session_state.last_result is not None:
    st.markdown('<div class="battle-area">', unsafe_allow_html=True)
    
    # Display choices
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown(f'<div class="choice-display">{CHOICES[st.session_state.player_choice]}</div>', unsafe_allow_html=True)
        st.markdown("**You**", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="font-size: 3rem; margin: 1rem;">⚔️</div>', unsafe_allow_html=True)
        st.markdown("**VS**")
    
    with col3:
        st.markdown(f'<div class="choice-display">{CHOICES[st.session_state.computer_choice]}</div>', unsafe_allow_html=True)
        st.markdown("**Computer**")
    
    # Result display
    result_class = st.session_state.last_result
    if st.session_state.last_result == "win":
        result_text = "🎉 You Win!"
        result_class = "win"
    elif st.session_state.last_result == "lose":
        result_text = "💻 Computer Wins!"
        result_class = "lose"
    else:
        result_text = "🤝 It's a Tie!"
        result_class = "tie"
    
    st.markdown(f'<div class="result-text {result_class}">{result_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Game statistics
if st.session_state.total_games > 0:
    win_rate = get_win_percentage()
    
    st.markdown(f"""
    <div class="stats-container">
        <h3>📊 Game Statistics</h3>
        <div style="display: flex; justify-content: space-around; margin: 1rem 0;">
            <div><strong>Win Rate:</strong> {win_rate:.1f}%</div>
            <div><strong>Best Streak:</strong> Coming Soon!</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Game history
    if st.session_state.game_history:
        with st.expander("📜 Recent Game History", expanded=False):
            for game in reversed(st.session_state.game_history[-5:]):  # Show last 5 games
                result_emoji = "🏆" if game['result'] == 'win' else "❌" if game['result'] == 'lose' else "🤝"
                st.write(f"Round {game['round']}: You ({CHOICES[game['player']]}) vs Computer ({CHOICES[game['computer']]}) {result_emoji}")

# Control buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset Game", use_container_width=True):
        reset_game()
        st.rerun()

with col2:
    if st.button("📊 View Stats", use_container_width=True):
        if st.session_state.total_games > 0:
            st.balloons()
            st.success(f"🎮 Games Played: {st.session_state.total_games} | Win Rate: {get_win_percentage():.1f}%")

st.markdown('</div>', unsafe_allow_html=True)

# Game rules
with st.expander("📋 Game Rules", expanded=False):
    st.markdown("""
    ### How to Play:
    - **Rock** 🪨 beats **Scissors** ✂️
    - **Scissors** ✂️ beats **Paper** 📄  
    - **Paper** 📄 beats **Rock** 🪨
    
    ### Scoring:
    - Win: +1 point to your score
    - Lose: +1 point to computer's score
    - Tie: +1 to tie count
    
    ### Tips:
    - 🎯 Try to identify patterns (though the computer is random!)
    - 🏆 Aim for a high win percentage
    - 🔄 Use reset to start fresh anytime
    """)

# Fun facts
with st.expander("🎲 Fun Facts", expanded=False):
    st.markdown("""
    ### Did You Know?
    - 🌍 Rock Paper Scissors is known worldwide with different names
    - 🧠 There are actually strategies to playing optimally
    - 🏆 There's a World Rock Paper Scissors Championship!
    - 🎮 The game is over 2000 years old
    - 🤖 True randomness is hard - even computers use algorithms!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.7); padding: 1rem;'>
    🎮 Rock Paper Scissors Game | Made with ❤️ using Streamlit | May the best player win! 🏆
</div>
""", unsafe_allow_html=True)