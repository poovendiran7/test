import streamlit as st
import random
import time
import json

# Configure page
st.set_page_config(
    page_title="🐍 Snake Adventure",
    page_icon="🐍",
    layout="wide"
)

# Custom CSS for kids-friendly design
st.markdown("""
<style>
    /* Import fun fonts */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One:wght@400&family=Comic+Neue:wght@400;700&display=swap');
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none;}
    .block-container {padding-top: 1rem !important;}
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #f9ca24, #f0932b, #eb4d4b);
        background-size: 400% 400%;
        animation: gradientShift 10s ease infinite;
        font-family: 'Comic Neue', cursive;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Game container */
    .game-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 2rem;
        margin: 1rem auto;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        border: 3px solid #fff;
        max-width: 800px;
        animation: containerBounce 3s ease-in-out infinite;
    }
    
    @keyframes containerBounce {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    /* Title styling */
    .game-title {
        font-family: 'Fredoka One', cursive;
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: titleWiggle 2s ease-in-out infinite;
    }
    
    @keyframes titleWiggle {
        0%, 100% { transform: rotate(-2deg); }
        50% { transform: rotate(2deg); }
    }
    
    /* Score and info styling */
    .game-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        animation: infoPulse 3s ease-in-out infinite;
    }
    
    @keyframes infoPulse {
        0%, 100% { box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        50% { box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
    }
    
    .score-item {
        text-align: center;
        font-weight: bold;
    }
    
    .score-number {
        font-size: 2rem;
        font-family: 'Fredoka One', cursive;
        display: block;
        animation: scoreJump 0.5s ease-in-out;
    }
    
    @keyframes scoreJump {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .score-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Game board styling */
    .game-board {
        display: grid;
        gap: 2px;
        background: #2c3e50;
        padding: 10px;
        border-radius: 20px;
        margin: 1rem auto;
        box-shadow: inset 0 4px 8px rgba(0,0,0,0.3);
        max-width: fit-content;
    }
    
    .game-cell {
        width: 25px;
        height: 25px;
        border-radius: 6px;
        transition: all 0.2s ease;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    
    .empty-cell {
        background: linear-gradient(135deg, #a8e6cf 0%, #88d8c0 100%);
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.3);
    }
    
    .snake-head {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        box-shadow: 0 3px 8px rgba(0,0,0,0.3);
        animation: snakeHeadPulse 1s ease-in-out infinite;
        z-index: 10;
    }
    
    @keyframes snakeHeadPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .snake-body {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        animation: snakeBodyWave 2s ease-in-out infinite;
    }
    
    @keyframes snakeBodyWave {
        0%, 100% { transform: scale(0.9); }
        50% { transform: scale(1); }
    }
    
    .food-cell {
        background: linear-gradient(135deg, #ff9ff3 0%, #54a0ff 100%);
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        animation: foodGlow 1.5s ease-in-out infinite;
        z-index: 5;
    }
    
    @keyframes foodGlow {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        50% { 
            transform: scale(1.2);
            box-shadow: 0 6px 20px rgba(255, 159, 243, 0.6);
        }
    }
    
    /* Control buttons */
    .controls-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .direction-controls {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
        gap: 0.5rem;
        max-width: 200px;
    }
    
    .control-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        padding: 0.6rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.2) !important;
        cursor: pointer !important;
        min-height: 45px !important;
        min-width: 45px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .control-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.3) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .control-btn:active {
        transform: translateY(0) !important;
        animation: buttonPress 0.1s ease-in-out !important;
    }
    
    @keyframes buttonPress {
        0% { transform: scale(1); }
        50% { transform: scale(0.95); }
        100% { transform: scale(1); }
    }
    
    /* Action buttons */
    .action-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .start-btn button {
        background: linear-gradient(135deg, #2ed573 0%, #1e90ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 0.8rem 2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        animation: startButtonGlow 2s ease-in-out infinite !important;
    }
    
    @keyframes startButtonGlow {
        0%, 100% { box-shadow: 0 4px 15px rgba(46, 213, 115, 0.3); }
        50% { box-shadow: 0 6px 25px rgba(46, 213, 115, 0.5); }
    }
    
    .restart-btn button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 0.8rem 2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* Game over modal */
    .game-over-modal {
        background: rgba(0, 0, 0, 0.8);
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .game-over-content {
        background: white;
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        animation: modalBounce 0.5s ease-out;
        max-width: 400px;
        margin: 1rem;
    }
    
    @keyframes modalBounce {
        0% { transform: scale(0.8); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .game-over-title {
        font-family: 'Fredoka One', cursive;
        font-size: 2.5rem;
        color: #ff6b6b;
        margin-bottom: 1rem;
        animation: shakeTitle 0.5s ease-in-out infinite alternate;
    }
    
    @keyframes shakeTitle {
        0% { transform: rotate(-1deg); }
        100% { transform: rotate(1deg); }
    }
    
    /* Instructions */
    .instructions {
        background: linear-gradient(135deg, #a8e6cf 0%, #88d8c0 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 2px solid #fff;
    }
    
    .instruction-title {
        font-family: 'Fredoka One', cursive;
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .instruction-item {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        font-size: 1rem;
        color: #2c3e50;
    }
    
    .instruction-emoji {
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    
    /* Responsive design */
    @media (max-width: 600px) {
        .game-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .game-title {
            font-size: 2rem;
        }
        
        .game-cell {
            width: 20px;
            height: 20px;
            font-size: 14px;
        }
        
        .direction-controls {
            max-width: 150px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize game state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.snake = [(10, 10)]
    st.session_state.direction = 'RIGHT'
    st.session_state.food = (15, 15)
    st.session_state.board_size = 20
    st.session_state.high_score = 0

# Game constants
BOARD_SIZE = st.session_state.board_size
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

def generate_food():
    """Generate food at a random position not occupied by snake"""
    while True:
        food_pos = (random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1))
        if food_pos not in st.session_state.snake:
            return food_pos

def move_snake():
    """Move the snake in the current direction"""
    head_x, head_y = st.session_state.snake[0]
    dx, dy = DIRECTIONS[st.session_state.direction]
    new_head = (head_x + dx, head_y + dy)
    
    # Check wall collision
    if (new_head[0] < 0 or new_head[0] >= BOARD_SIZE or 
        new_head[1] < 0 or new_head[1] >= BOARD_SIZE):
        return False
    
    # Check self collision
    if new_head in st.session_state.snake:
        return False
    
    # Add new head
    st.session_state.snake.insert(0, new_head)
    
    # Check if food is eaten
    if new_head == st.session_state.food:
        st.session_state.score += 10
        st.session_state.food = generate_food()
        # Update high score
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
    else:
        # Remove tail if no food eaten
        st.session_state.snake.pop()
    
    return True

def reset_game():
    """Reset the game to initial state"""
    st.session_state.game_started = False
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.snake = [(10, 10)]
    st.session_state.direction = 'RIGHT'
    st.session_state.food = generate_food()

def start_game():
    """Start the game"""
    st.session_state.game_started = True
    st.session_state.game_over = False

def change_direction(new_direction):
    """Change snake direction if valid"""
    opposite_directions = {
        'UP': 'DOWN',
        'DOWN': 'UP',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT'
    }
    
    # Don't allow reverse direction
    if new_direction != opposite_directions.get(st.session_state.direction):
        st.session_state.direction = new_direction

def render_game_board():
    """Render the game board as HTML"""
    board_html = f'<div class="game-board" style="grid-template-columns: repeat({BOARD_SIZE}, 1fr);">'
    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            pos = (x, y)
            cell_class = "empty-cell"
            cell_content = ""
            
            if pos == st.session_state.snake[0]:  # Snake head
                cell_class = "snake-head"
                cell_content = "🐍"
            elif pos in st.session_state.snake[1:]:  # Snake body
                cell_class = "snake-body"
                cell_content = "🟢"
            elif pos == st.session_state.food:  # Food
                cell_class = "food-cell"
                food_emojis = ["🍎", "🍌", "🍇", "🍓", "🥕", "🍕", "🍔", "🍩"]
                cell_content = random.choice(food_emojis)
            
            board_html += f'<div class="game-cell {cell_class}">{cell_content}</div>'
    
    board_html += '</div>'
    return board_html

# Main game container
st.markdown('<div class="game-container">', unsafe_allow_html=True)

# Game title
st.markdown('<h1 class="game-title">🐍 Snake Adventure!</h1>', unsafe_allow_html=True)

# Game info bar
st.markdown(f'''
<div class="game-info">
    <div class="score-item">
        <span class="score-number">{st.session_state.score}</span>
        <span class="score-label">Score</span>
    </div>
    <div class="score-item">
        <span class="score-number">{st.session_state.high_score}</span>
        <span class="score-label">High Score</span>
    </div>
    <div class="score-item">
        <span class="score-number">{len(st.session_state.snake)}</span>
        <span class="score-label">Length</span>
    </div>
    <div class="score-item">
        <span class="score-number">{"🎮" if st.session_state.game_started else "⏸️"}</span>
        <span class="score-label">Status</span>
    </div>
</div>
''', unsafe_allow_html=True)

# Game board
if not st.session_state.game_over:
    st.markdown(render_game_board(), unsafe_allow_html=True)

# Control buttons
st.markdown('<div class="controls-container">', unsafe_allow_html=True)

# Direction controls
st.markdown('<div class="direction-controls">', unsafe_allow_html=True)

# Top row - UP button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("⬆️", key="up", disabled=not st.session_state.game_started or st.session_state.game_over):
        change_direction('UP')

# Middle row - LEFT and RIGHT buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("⬅️", key="left", disabled=not st.session_state.game_started or st.session_state.game_over):
        change_direction('LEFT')
with col3:
    if st.button("➡️", key="right", disabled=not st.session_state.game_started or st.session_state.game_over):
        change_direction('RIGHT')

# Bottom row - DOWN button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("⬇️", key="down", disabled=not st.session_state.game_started or st.session_state.game_over):
        change_direction('DOWN')

st.markdown('</div>', unsafe_allow_html=True)

# Action buttons
st.markdown('<div class="action-buttons">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if not st.session_state.game_started:
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("🚀 Start Game!", key="start_game"):
            start_game()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="restart-btn">', unsafe_allow_html=True)
    if st.button("🔄 Restart Game", key="restart_game"):
        reset_game()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Instructions
st.markdown('''
<div class="instructions">
    <h3 class="instruction-title">🎯 How to Play</h3>
    <div class="instruction-item">
        <span class="instruction-emoji">🐍</span>
        <span>Control the green snake using the arrow buttons!</span>
    </div>
    <div class="instruction-item">
        <span class="instruction-emoji">🍎</span>
        <span>Eat the colorful food to grow bigger and score points!</span>
    </div>
    <div class="instruction-item">
        <span class="instruction-emoji">⚠️</span>
        <span>Don't hit the walls or your own tail!</span>
    </div>
    <div class="instruction-item">
        <span class="instruction-emoji">🏆</span>
        <span>Try to beat your high score and grow as long as possible!</span>
    </div>
    <div class="instruction-item">
        <span class="instruction-emoji">🎮</span>
        <span>Click Start Game to begin your snake adventure!</span>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Game over modal
if st.session_state.game_over:
    encouragement_messages = [
        "Great job! 🌟",
        "You're awesome! 🎉",
        "Keep trying! 💪",
        "Almost there! 🚀",
        "Super effort! ⭐",
        "You rock! 🎸",
        "Fantastic! 🎊",
        "Well done! 👏"
    ]
    
    st.markdown(f'''
    <div class="game-over-modal">
        <div class="game-over-content">
            <h2 class="game-over-title">Game Over! 🎮</h2>
            <p style="font-size: 1.5rem; margin: 1rem 0;">
                {random.choice(encouragement_messages)}
            </p>
            <p style="font-size: 1.2rem; color: #667eea; margin-bottom: 2rem;">
                Final Score: <strong>{st.session_state.score}</strong> points<br>
                Snake Length: <strong>{len(st.session_state.snake)}</strong> blocks
            </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Play Again button (outside the modal HTML)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 Play Again!", key="play_again_modal", use_container_width=True):
            reset_game()
            start_game()
            st.rerun()

# Game loop - move snake automatically when game is running
if st.session_state.game_started and not st.session_state.game_over:
    time.sleep(0.3)  # Game speed
    if not move_snake():
        st.session_state.game_over = True
    st.rerun()

# Sidebar with game stats and tips
with st.sidebar:
    st.markdown("## 🎮 Snake Adventure Stats")
    
    st.markdown(f"""
    **🏆 Current Session:**
    - Score: {st.session_state.score}
    - Length: {len(st.session_state.snake)}
    - High Score: {st.session_state.high_score}
    
    **🐍 Snake Status:**
    - Direction: {st.session_state.direction}
    - Position: {st.session_state.snake[0] if st.session_state.snake else 'N/A'}
    """)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Pro Tips!")
    st.markdown("""
    - 🚀 **Start Slow**: Take your time to plan moves
    - 🔄 **Use Corners**: Corner movements help avoid collisions
    - 🎯 **Plan Ahead**: Think about where you'll go next
    - 🌟 **Stay Calm**: Don't panic when the snake gets long
    - 🍎 **Food Strategy**: Sometimes wait for better food positions
    """)
    
    st.markdown("---")
    
    st.markdown("## 🌈 Fun Facts!")
    st.markdown("""
    - 🐍 Snakes can't move backwards!
    - 🍎 Each food gives you 10 points
    - 🏆 Your high score is saved during your session
    - 🎮 The game gets trickier as you grow
    - 🌟 There are different food emojis to collect!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #667eea; padding: 1rem; font-family: "Comic Neue", cursive;'>
    🐍 <strong>Snake Adventure v1.0</strong> 🐍<br>
    Made with ❤️ for kids of all ages! Have fun playing! 🎮✨
</div>
""", unsafe_allow_html=True)