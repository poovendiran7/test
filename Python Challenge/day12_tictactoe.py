import streamlit as st
import random
import time

# Configure page
st.set_page_config(
    page_title="🎮 Tic-Tac-Toe",
    page_icon="🎮",
    layout="centered"
)

# Custom CSS for dark theme and animations
st.markdown("""
<style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    .main-title {
        text-align: center;
        color: #00ff88;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px #00ff88;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px #00ff88; }
        to { text-shadow: 0 0 30px #00ff88, 0 0 40px #00ff88; }
    }
    
    .winner-animation {
        text-align: center;
        font-size: 2.5rem;
        color: #ffd700;
        font-weight: bold;
        animation: bounce 0.6s ease infinite;
        margin: 1rem 0;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(-10px); }
    }
    
    .game-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .game-board {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 2rem auto;
        max-width: 400px;
    }
    
    .board-row {
        display: flex;
        width: 100%;
        margin: 0;
    }
    
    .stButton > button {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 3px solid #444 !important;
        border-radius: 0 !important;
        font-size: 2.5rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        height: 120px !important;
        width: 120px !important;
        min-height: 120px !important;
        min-width: 120px !important;
        max-height: 120px !important;
        max-width: 120px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stButton {
        flex: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stButton > button:hover {
        border-color: #00ff88 !important;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3) !important;
        background-color: #3d3d3d !important;
    }
    
    .stButton > button:disabled {
        opacity: 1 !important;
        background-color: #2d2d2d !important;
    }
    
    /* Remove gaps between cells */
    .board-row .stButton:first-child > button {
        border-right: 1.5px solid #444 !important;
    }
    
    .board-row .stButton:last-child > button {
        border-left: 1.5px solid #444 !important;
    }
    
    .board-row .stButton:nth-child(2) > button {
        border-left: 1.5px solid #444 !important;
        border-right: 1.5px solid #444 !important;
    }
    
    .board-row:first-child .stButton > button {
        border-bottom: 1.5px solid #444 !important;
    }
    
    .board-row:last-child .stButton > button {
        border-top: 1.5px solid #444 !important;
    }
    
    .board-row:nth-child(2) .stButton > button {
        border-top: 1.5px solid #444 !important;
        border-bottom: 1.5px solid #444 !important;
    }
    
    .winning-cell {
        animation: flash 0.8s ease-in-out infinite alternate;
    }
    
    @keyframes flash {
        from { background-color: #ffd700; }
        to { background-color: #ff6b6b; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = []
    st.session_state.game_mode = 'Two Player'
    st.session_state.scores = {'X': 0, 'O': 0, 'Draws': 0}

def check_winner(board):
    """Check if there's a winner and return the winner and winning line"""
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != '':
            return board[0][j], [(0, j), (1, j), (2, j)]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    
    return None, []

def is_board_full(board):
    """Check if the board is full"""
    return all(board[i][j] != '' for i in range(3) for j in range(3))

def get_computer_move(board):
    """Get a random valid move for the computer"""
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    return random.choice(empty_cells) if empty_cells else None

def make_move(row, col):
    """Make a move on the board"""
    if st.session_state.board[row][col] == '' and not st.session_state.game_over:
        st.session_state.board[row][col] = st.session_state.current_player
        
        # Check for winner
        winner, winning_line = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
            st.session_state.winning_line = winning_line
            st.session_state.scores[winner] += 1
        elif is_board_full(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = 'Draw'
            st.session_state.scores['Draws'] += 1
        else:
            # Switch player
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
            
            # Computer move if in computer mode and it's O's turn
            if (st.session_state.game_mode == 'vs Computer' and 
                st.session_state.current_player == 'O' and 
                not st.session_state.game_over):
                
                time.sleep(0.5)  # Small delay for better UX
                comp_row, comp_col = get_computer_move(st.session_state.board)
                if comp_row is not None:
                    st.session_state.board[comp_row][comp_col] = 'O'
                    
                    # Check for winner after computer move
                    winner, winning_line = check_winner(st.session_state.board)
                    if winner:
                        st.session_state.game_over = True
                        st.session_state.winner = winner
                        st.session_state.winning_line = winning_line
                        st.session_state.scores[winner] += 1
                    elif is_board_full(st.session_state.board):
                        st.session_state.game_over = True
                        st.session_state.winner = 'Draw'
                        st.session_state.scores['Draws'] += 1
                    else:
                        st.session_state.current_player = 'X'

def reset_game():
    """Reset the game board"""
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = []

# Title
st.markdown('<h1 class="main-title">🎮 TIC-TAC-TOE 🎮</h1>', unsafe_allow_html=True)

# Game mode selection
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    game_mode = st.selectbox(
        "🎯 Select Game Mode:",
        ["Two Player", "vs Computer"],
        index=0 if st.session_state.game_mode == "Two Player" else 1
    )
    if game_mode != st.session_state.game_mode:
        st.session_state.game_mode = game_mode
        reset_game()

# Score display
st.markdown(f"""
<div class="game-stats">
    🏆 <strong>Scores:</strong> X: {st.session_state.scores['X']} | O: {st.session_state.scores['O']} | Draws: {st.session_state.scores['Draws']}
</div>
""", unsafe_allow_html=True)

# Current player display
if not st.session_state.game_over:
    player_emoji = "❌" if st.session_state.current_player == 'X' else "⭕"
    st.markdown(f"<h3 style='text-align: center; color: #00ff88;'>Current Player: {player_emoji} {st.session_state.current_player}</h3>", 
                unsafe_allow_html=True)

# Winner announcement with animation
if st.session_state.game_over and st.session_state.winner:
    if st.session_state.winner == 'Draw':
        st.markdown('<div class="winner-animation">🤝 It\'s a Draw! 🤝</div>', unsafe_allow_html=True)
    else:
        winner_emoji = "❌" if st.session_state.winner == 'X' else "⭕"
        st.markdown(f'<div class="winner-animation">🎉 Player {st.session_state.winner} {winner_emoji} Wins! 🎉</div>', 
                    unsafe_allow_html=True)

# Game board
st.markdown("### 🎲 Game Board")
st.markdown('<div class="game-board">', unsafe_allow_html=True)

for i in range(3):
    st.markdown('<div class="board-row">', unsafe_allow_html=True)
    cols = st.columns([1, 1, 1], gap="small")
    
    for j in range(3):
        with cols[j]:
            # Determine button style and content
            cell_value = st.session_state.board[i][j]
            button_text = "　"  # Wide space for empty cells
            
            # Add emoji for X and O
            if cell_value == 'X':
                button_text = "❌"
            elif cell_value == 'O':
                button_text = "⭕"
            
            # Check if this cell is part of winning line
            is_winning_cell = (i, j) in st.session_state.winning_line
            
            # Create button with special styling for winning cells
            button_key = f"btn_{i}_{j}"
            if st.button(
                button_text,
                key=button_key,
                help=f"Row {i+1}, Column {j+1}",
                disabled=cell_value != '' or st.session_state.game_over
            ):
                make_move(i, j)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Control buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔄 Reset Game", help="Start a new game"):
        reset_game()
        st.rerun()

with col2:
    if st.button("🗑️ Clear Scores", help="Reset all scores to zero"):
        st.session_state.scores = {'X': 0, 'O': 0, 'Draws': 0}
        st.rerun()

with col3:
    if st.button("🎲 New Round", help="Start new round (keep scores)"):
        reset_game()
        st.rerun()

# Game instructions
with st.expander("📖 How to Play", expanded=False):
    st.markdown("""
    **🎯 Objective:** Get three of your marks (X or O) in a row, column, or diagonal.
    
    **🎮 Two Player Mode:** Players take turns clicking empty squares.
    
    **🤖 vs Computer Mode:** You play as X, computer plays as O with random moves.
    
    **✨ Features:**
    - 🎨 Dark theme with glowing effects
    - 🏆 Score tracking across multiple games
    - 🌟 Winning animations and highlights
    - 🔄 Easy reset and new game options
    
    **💡 Tips:**
    - Control the center square for better winning chances
    - Block your opponent's winning moves
    - Look for opportunities to create multiple winning threats
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    Made with ❤️ using Streamlit | 🎮 Have fun playing!
</div>
""", unsafe_allow_html=True)