import streamlit as st
import random
import string
import math

# Game configuration
WHEEL_VALUES = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, "BANKRUPT", "LOSE A TURN"]
VOWELS = set('AEIOU')
VOWEL_COST = 250

# Sample puzzles (category: puzzle)
PUZZLES = {
    "Things": [
        "LAPTOP COMPUTER", "BEACH UMBRELLA", "COFFEE MAKER", "RUNNING SHOES",
        "ELECTRIC GUITAR", "WEDDING RING", "BASKETBALL HOOP", "KITCHEN SINK",
        "ROCKING CHAIR", "FIRE EXTINGUISHER", "WASHING MACHINE", "CEILING FAN",
        "CAMPING TENT", "FISHING ROD", "VACUUM CLEANER", "CEILING LAMP",
        "TOOL BOX", "PHOTO ALBUM", "CUTTING BOARD", "GARDEN HOSE",
        "WELCOME MAT", "ROLLING PIN", "ALARM CLOCK", "PAPER TOWEL",
        "CHOCOLATE CHIP COOKIE", "BREAKFAST CEREAL", "SWIMMING POOL",
        "PARKING METER", "SHOWER CURTAIN", "DINING TABLE", "KING SIZE BED"
    ],
    "Places": [
        "EIFFEL TOWER", "GRAND CANYON", "TIMES SQUARE", "GOLDEN GATE BRIDGE",
        "NIAGARA FALLS", "STATUE OF LIBERTY", "MOUNT RUSHMORE", "YELLOWSTONE PARK",
        "DISNEY WORLD", "LAS VEGAS STRIP", "HOLLYWOOD BOULEVARD", "CENTRAL PARK",
        "BUCKINGHAM PALACE", "GREAT WALL OF CHINA", "PYRAMIDS OF EGYPT", "TAJ MAHAL",
        "SYDNEY OPERA HOUSE", "BIG BEN", "COLOSSEUM", "STONEHENGE",
        "MOUNT EVEREST", "AMAZON RAINFOREST", "SAHARA DESERT", "NORTH POLE",
        "SOUTH POLE", "PACIFIC OCEAN", "ATLANTIC OCEAN", "ROCKY MOUNTAINS",
        "VENICE CANALS", "PARIS FRANCE", "LONDON ENGLAND", "TOKYO JAPAN",
        "NEW YORK CITY", "SAN FRANCISCO", "MIAMI BEACH", "BOSTON HARBOR"
    ],
    "Phrase": [
        "BETTER LATE THAN NEVER", "PRACTICE MAKES PERFECT", "ACTIONS SPEAK LOUDER THAN WORDS",
        "THE EARLY BIRD GETS THE WORM", "WHEN PIGS FLY", "BREAK A LEG",
        "PIECE OF CAKE", "HIT THE NAIL ON THE HEAD", "COST AN ARM AND A LEG",
        "ONCE IN A BLUE MOON", "BITE THE BULLET", "LET THE CAT OUT OF THE BAG",
        "SPILL THE BEANS", "BREAK THE ICE", "CUTTING CORNERS", "BEAT AROUND THE BUSH",
        "CAUGHT RED HANDED", "EVERY CLOUD HAS A SILVER LINING", "EASIER SAID THAN DONE",
        "KILL TWO BIRDS WITH ONE STONE", "THE BALL IS IN YOUR COURT", "BACK TO SQUARE ONE",
        "BLESSING IN DISGUISE", "CALL IT A DAY", "GET YOUR ACT TOGETHER",
        "HANG IN THERE", "NO PAIN NO GAIN", "TIME FLIES WHEN HAVING FUN",
        "THE BEST OF BOTH WORLDS", "YOU CANT JUDGE A BOOK BY ITS COVER",
        "BURNING THE MIDNIGHT OIL", "A DIME A DOZEN", "GET OUT OF HAND"
    ],
    "Person": [
        "ALBERT EINSTEIN", "WILLIAM SHAKESPEARE", "LEONARDO DA VINCI",
        "ABRAHAM LINCOLN", "GEORGE WASHINGTON", "BENJAMIN FRANKLIN", "THOMAS EDISON",
        "MARTIN LUTHER KING", "MICHAEL JORDAN", "MUHAMMAD ALI", "BABE RUTH",
        "WALT DISNEY", "OPRAH WINFREY", "STEVEN SPIELBERG", "STEVE JOBS",
        "BILL GATES", "MARK TWAIN", "ERNEST HEMINGWAY", "MAYA ANGELOU",
        "ELVIS PRESLEY", "MICHAEL JACKSON", "FRANK SINATRA", "MARILYN MONROE",
        "AMELIA EARHART", "NEIL ARMSTRONG", "ROSA PARKS", "HELEN KELLER",
        "CHARLES DARWIN", "ISAAC NEWTON", "MARIE CURIE", "FLORENCE NIGHTINGALE",
        "CLEOPATRA", "JULIUS CAESAR", "CHRISTOPHER COLUMBUS", "GALILEO GALILEI"
    ],
    "Food & Drink": [
        "CHOCOLATE CAKE", "PEPPERONI PIZZA", "CHEESEBURGER AND FRIES", "SPAGHETTI AND MEATBALLS",
        "CHICKEN NOODLE SOUP", "GRILLED CHEESE SANDWICH", "SCRAMBLED EGGS", "PANCAKES AND SYRUP",
        "HOT FUDGE SUNDAE", "APPLE PIE", "STRAWBERRY SHORTCAKE", "PEANUT BUTTER AND JELLY",
        "MACARONI AND CHEESE", "CHOCOLATE CHIP COOKIES", "FISH AND CHIPS", "BACON AND EGGS",
        "ROAST TURKEY", "MASHED POTATOES", "CAESAR SALAD", "FRENCH TOAST",
        "ICE CREAM CONE", "FRIED CHICKEN", "BEEF TACOS", "CHEESE PIZZA",
        "ORANGE JUICE", "CHOCOLATE MILK", "ICED COFFEE", "GREEN TEA"
    ],
    "Occupation": [
        "FIREFIGHTER", "POLICE OFFICER", "SCHOOL TEACHER", "NURSE PRACTITIONER",
        "BRAIN SURGEON", "ROCKET SCIENTIST", "PROFESSIONAL ATHLETE", "MOVIE STAR",
        "FASHION DESIGNER", "COMPUTER PROGRAMMER", "CIVIL ENGINEER", "ACCOUNTANT",
        "REAL ESTATE AGENT", "CONSTRUCTION WORKER", "AIRPLANE PILOT", "DELIVERY DRIVER",
        "HAIR STYLIST", "PERSONAL TRAINER", "WEDDING PLANNER", "INTERIOR DECORATOR",
        "VETERINARIAN", "DENTIST", "PHARMACIST", "LIBRARIAN", "CHEF", "ARCHITECT"
    ],
    "Movie Title": [
        "THE WIZARD OF OZ", "STAR WARS", "JURASSIC PARK", "FORREST GUMP",
        "THE LION KING", "FINDING NEMO", "TOY STORY", "FROZEN",
        "THE GODFATHER", "TITANIC", "AVATAR", "THE AVENGERS",
        "BACK TO THE FUTURE", "INDIANA JONES", "ROCKY", "JAWS",
        "THE DARK KNIGHT", "HARRY POTTER", "LORD OF THE RINGS", "GLADIATOR",
        "THE MATRIX", "PULP FICTION", "CASABLANCA", "GONE WITH THE WIND"
    ],
    "Before & After": [
        "MAPLE SYRUP BOTTLE", "FRENCH FRY PAN", "ALARM CLOCK TOWER",
        "FIRE TRUCK STOP", "PEANUT BUTTER CUP HOLDER", "BIRTHDAY CAKE WALK",
        "GRAND PIANO KEYS", "TENNIS BALL ROOM", "HONEY BEE HIVE MIND",
        "SWIMMING POOL TABLE", "ROLLER COASTER RIDE SHARE", "BUBBLE GUM DROP"
    ]
}

def initialize_game_state():
    """Initialize or reset game state"""
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'num_players' not in st.session_state:
        st.session_state.num_players = 2
    if 'players' not in st.session_state:
        st.session_state.players = []
    if 'current_player_idx' not in st.session_state:
        st.session_state.current_player_idx = 0
    if 'puzzle' not in st.session_state:
        st.session_state.puzzle = ""
    if 'category' not in st.session_state:
        st.session_state.category = ""
    if 'guessed_letters' not in st.session_state:
        st.session_state.guessed_letters = set()
    if 'wheel_value' not in st.session_state:
        st.session_state.wheel_value = None
    if 'game_message' not in st.session_state:
        st.session_state.game_message = ""
    if 'wheel_rotation' not in st.session_state:
        st.session_state.wheel_rotation = 0

def start_new_game():
    """Start a new game with selected number of players"""
    st.session_state.game_started = True
    st.session_state.players = [
        {'name': f'Player {i+1}', 'score': 0, 'round_earnings': 0}
        for i in range(st.session_state.num_players)
    ]
    st.session_state.current_player_idx = 0
    st.session_state.guessed_letters = set()
    st.session_state.wheel_value = None
    st.session_state.game_message = ""
    
    # Select random puzzle
    category = random.choice(list(PUZZLES.keys()))
    puzzle = random.choice(PUZZLES[category])
    st.session_state.category = category
    st.session_state.puzzle = puzzle.upper()

def spin_wheel():
    """Spin the wheel and return a value"""
    return random.choice(WHEEL_VALUES)

def display_puzzle():
    """Display the puzzle with guessed letters revealed"""
    html_output = '<div style="text-align: center; font-family: monospace; font-size: 48px; font-weight: bold; letter-spacing: 8px; margin: 30px 0;">'
    
    for char in st.session_state.puzzle:
        if char == ' ':
            html_output += '<span style="margin: 0 20px;"></span>'
        elif char in string.ascii_uppercase and char not in st.session_state.guessed_letters:
            html_output += '<span style="color: #ddd; border-bottom: 4px solid #333; padding: 0 8px; margin: 0 4px;">_</span>'
        else:
            # Guessed letters are shown in bright color
            html_output += f'<span style="color: #4CAF50; border-bottom: 4px solid #4CAF50; padding: 0 8px; margin: 0 4px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{char}</span>'
    
    html_output += '</div>'
    return html_output

def create_wheel_svg(rotation_angle=0):
    """Create an SVG representation of the wheel"""
    segments = len(WHEEL_VALUES)
    angle_per_segment = 360 / segments
    radius = 150
    center = 160
    
    # Colors for different segment types
    colors = []
    for value in WHEEL_VALUES:
        if value == "BANKRUPT":
            colors.append("#000000")
        elif value == "LOSE A TURN":
            colors.append("#FF6B6B")
        elif value >= 700:
            colors.append("#FFD700")  # Gold
        elif value >= 400:
            colors.append("#4CAF50")  # Green
        else:
            colors.append("#2196F3")  # Blue
    
    # Start SVG
    svg = f'<svg width="320" height="320" viewBox="0 0 320 320" style="margin: 20px auto; display: block;">'
    
    # Apply rotation
    svg += f'<g id="wheel" transform="rotate({rotation_angle} {center} {center})">'
    
    # Draw segments
    for i, (value, color) in enumerate(zip(WHEEL_VALUES, colors)):
        start_angle = i * angle_per_segment - 90  # Start from top
        end_angle = start_angle + angle_per_segment
        
        # Calculate path for segment
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        x1 = center + radius * math.cos(start_rad)
        y1 = center + radius * math.sin(start_rad)
        x2 = center + radius * math.cos(end_rad)
        y2 = center + radius * math.sin(end_rad)
        
        # Create segment path
        large_arc = 1 if angle_per_segment > 180 else 0
        path = f'M {center} {center} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z'
        
        svg += f'<path d="{path}" fill="{color}" stroke="#FFF" stroke-width="2"/>'
        
        # Add text label
        mid_angle = start_angle + angle_per_segment / 2
        mid_rad = math.radians(mid_angle)
        text_radius = radius * 0.7
        text_x = center + text_radius * math.cos(mid_rad)
        text_y = center + text_radius * math.sin(mid_rad)
        
        text_color = "#FFF"
        font_size = "9" if isinstance(value, str) else "13"
        font_weight = "bold"
        
        # Format display text
        if isinstance(value, str):
            # Split long text into two lines for special spaces
            if value == "LOSE A TURN":
                display_text = ["LOSE", "TURN"]
            else:
                display_text = [value]
        else:
            display_text = [f"${value}"]
        
        # Render text (split into lines if needed)
        for idx, line in enumerate(display_text):
            offset_y = (idx - (len(display_text) - 1) / 2) * 12
            svg += f'<text x="{text_x}" y="{text_y + offset_y}" fill="{text_color}" font-size="{font_size}" font-weight="{font_weight}" text-anchor="middle" dominant-baseline="middle" transform="rotate({mid_angle + 90} {text_x} {text_y + offset_y})">'
            svg += line
            svg += '</text>'
    
    svg += '</g>'
    
    # Add center circle
    svg += f'<circle cx="{center}" cy="{center}" r="20" fill="#FFD700" stroke="#FFF" stroke-width="3"/>'
    svg += f'<circle cx="{center}" cy="{center}" r="10" fill="#FFF"/>'
    
    # Add pointer at top
    svg += f'<polygon points="{center},{center-radius-20} {center-15},{center-radius} {center+15},{center-radius}" fill="#FF0000" stroke="#000" stroke-width="2"/>'
    
    svg += '</svg>'
    
    return svg

def is_puzzle_solved():
    """Check if puzzle is completely solved"""
    for char in st.session_state.puzzle:
        if char in string.ascii_uppercase and char not in st.session_state.guessed_letters:
            return False
    return True

def guess_consonant(letter):
    """Handle consonant guess"""
    letter = letter.upper()
    
    if letter in st.session_state.guessed_letters:
        st.session_state.game_message = f"❌ {letter} has already been guessed!"
        return
    
    if letter in VOWELS:
        st.session_state.game_message = f"❌ {letter} is a vowel! Buy vowels separately."
        return
    
    st.session_state.guessed_letters.add(letter)
    count = st.session_state.puzzle.count(letter)
    
    current_player = st.session_state.players[st.session_state.current_player_idx]
    
    if count > 0:
        if isinstance(st.session_state.wheel_value, int):
            earnings = st.session_state.wheel_value * count
            current_player['round_earnings'] += earnings
            st.session_state.game_message = f"✅ Found {count} {letter}'s! Earned ${earnings}"
        else:
            st.session_state.game_message = f"✅ Found {count} {letter}'s!"
    else:
        st.session_state.game_message = f"❌ No {letter}'s in the puzzle. Next player's turn!"
        next_player()

def buy_vowel(letter):
    """Handle vowel purchase"""
    letter = letter.upper()
    current_player = st.session_state.players[st.session_state.current_player_idx]
    
    if letter in st.session_state.guessed_letters:
        st.session_state.game_message = f"❌ {letter} has already been guessed!"
        return
    
    if letter not in VOWELS:
        st.session_state.game_message = f"❌ {letter} is not a vowel!"
        return
    
    if current_player['round_earnings'] < VOWEL_COST:
        st.session_state.game_message = f"❌ Not enough money! Need ${VOWEL_COST}, have ${current_player['round_earnings']}"
        return
    
    current_player['round_earnings'] -= VOWEL_COST
    st.session_state.guessed_letters.add(letter)
    count = st.session_state.puzzle.count(letter)
    
    if count > 0:
        st.session_state.game_message = f"✅ Found {count} {letter}'s! Cost: ${VOWEL_COST}"
    else:
        st.session_state.game_message = f"❌ No {letter}'s in the puzzle. Next player's turn!"
        next_player()

def solve_puzzle(guess):
    """Handle puzzle solve attempt"""
    guess = guess.upper().strip()
    current_player = st.session_state.players[st.session_state.current_player_idx]
    
    if guess == st.session_state.puzzle:
        # Add round earnings to total score
        current_player['score'] += current_player['round_earnings']
        st.session_state.game_message = f"🎉 {current_player['name']} solved it! Won ${current_player['round_earnings']}!"
        # Reveal all letters
        for char in st.session_state.puzzle:
            if char in string.ascii_uppercase:
                st.session_state.guessed_letters.add(char)
    else:
        st.session_state.game_message = f"❌ Wrong answer! Next player's turn."
        next_player()

def next_player():
    """Move to next player and reset round earnings"""
    st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % st.session_state.num_players
    st.session_state.wheel_value = None

def handle_wheel_result(value):
    """Handle special wheel results"""
    current_player = st.session_state.players[st.session_state.current_player_idx]
    
    if value == "BANKRUPT":
        current_player['round_earnings'] = 0
        st.session_state.game_message = "💥 BANKRUPT! Lost all round earnings. Next player's turn!"
        next_player()
    elif value == "LOSE A TURN":
        st.session_state.game_message = "😞 LOSE A TURN! Next player's turn!"
        next_player()

# Main app
def main():
    st.set_page_config(page_title="Wheel of Fortune", page_icon="🎡", layout="wide")
    
    initialize_game_state()
    
    st.title("🎡 Wheel of Fortune")
    
    # Sidebar for game setup
    with st.sidebar:
        st.header("Game Setup")
        
        if not st.session_state.game_started:
            st.session_state.num_players = st.selectbox(
                "Number of Players",
                options=[1, 2, 3, 4],
                index=1
            )
            
            if st.button("Start New Game", type="primary", use_container_width=True):
                start_new_game()
                st.rerun()
        else:
            if st.button("New Game", type="primary", use_container_width=True):
                st.session_state.game_started = False
                st.rerun()
            
            st.divider()
            st.subheader("Scoreboard")
            for i, player in enumerate(st.session_state.players):
                if i == st.session_state.current_player_idx:
                    st.markdown(f"**👉 {player['name']}**")
                else:
                    st.markdown(f"{player['name']}")
                st.markdown(f"Total: ${player['score']}")
                st.markdown(f"Round: ${player['round_earnings']}")
                st.divider()
    
    # Main game area
    if not st.session_state.game_started:
        st.info("👈 Select number of players and click 'Start New Game' to begin!")
        st.markdown("""
        ### How to Play:
        1. **Spin the Wheel** to get a dollar amount or special action
        2. **Guess a Consonant** - If correct, earn money × number of letters
        3. **Buy a Vowel** - Costs $250 from your round earnings
        4. **Solve the Puzzle** - Win all your round earnings!
        
        **Special Wheel Spaces:**
        - 💥 **BANKRUPT** - Lose all round earnings
        - 😞 **LOSE A TURN** - Skip your turn
        """)
    else:
        # Display category and puzzle
        st.subheader(f"Category: {st.session_state.category}")
        st.markdown(display_puzzle(), unsafe_allow_html=True)
        
        # Display game message
        if st.session_state.game_message:
            if "✅" in st.session_state.game_message or "🎉" in st.session_state.game_message:
                st.success(st.session_state.game_message)
            else:
                st.warning(st.session_state.game_message)
        
        # Check if puzzle is solved
        if is_puzzle_solved():
            st.balloons()
            st.success("🎉 Puzzle Solved!")
            if st.button("Start New Round"):
                start_new_game()
                st.rerun()
            return
        
        # Current player info
        current_player = st.session_state.players[st.session_state.current_player_idx]
        st.info(f"**Current Turn: {current_player['name']}** | Round Earnings: ${current_player['round_earnings']}")
        
        # Game actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🎡 Spin Wheel")
            
            if st.button("SPIN!", type="primary", use_container_width=True):
                wheel_result = spin_wheel()
                st.session_state.wheel_value = wheel_result
                
                if isinstance(wheel_result, str):
                    handle_wheel_result(wheel_result)
                else:
                    st.session_state.game_message = f"🎡 Wheel landed on: ${wheel_result}"
                
                st.rerun()
            
            if st.session_state.wheel_value:
                if isinstance(st.session_state.wheel_value, int):
                    st.success(f"💰 Current Value: ${st.session_state.wheel_value}")
                else:
                    st.error(f"⚠️ {st.session_state.wheel_value}")
        
        with col2:
            st.subheader("🔤 Guess Consonant")
            available_consonants = [c for c in string.ascii_uppercase 
                                   if c not in VOWELS and c not in st.session_state.guessed_letters]
            
            if st.session_state.wheel_value and isinstance(st.session_state.wheel_value, int):
                consonant = st.selectbox("Select consonant:", available_consonants, key="consonant_select")
                if st.button("Guess Consonant", use_container_width=True):
                    guess_consonant(consonant)
                    st.rerun()
            else:
                st.info("Spin the wheel first!")
        
        with col3:
            st.subheader("💰 Buy Vowel")
            available_vowels = [v for v in VOWELS if v not in st.session_state.guessed_letters]
            
            vowel = st.selectbox("Select vowel:", available_vowels, key="vowel_select")
            if st.button(f"Buy Vowel (${VOWEL_COST})", use_container_width=True):
                buy_vowel(vowel)
                st.rerun()
        
        st.divider()
        
        # Solve puzzle
        st.subheader("🎯 Solve the Puzzle")
        col_solve1, col_solve2 = st.columns([3, 1])
        with col_solve1:
            puzzle_guess = st.text_input("Enter your solution:", key="puzzle_input")
        with col_solve2:
            st.write("")  # Spacing
            if st.button("Solve!", type="primary", use_container_width=True):
                if puzzle_guess:
                    solve_puzzle(puzzle_guess)
                    st.rerun()
        
        # Display guessed letters
        st.divider()
        
        # Show guessed letters in a more prominent way
        st.markdown("### 📝 Guessed Letters")
        if st.session_state.guessed_letters:
            # Separate consonants and vowels
            consonants = sorted([l for l in st.session_state.guessed_letters if l not in VOWELS])
            vowels_guessed = sorted([l for l in st.session_state.guessed_letters if l in VOWELS])
            
            col_c, col_v = st.columns(2)
            with col_c:
                st.markdown("**Consonants:**")
                consonant_html = '<div style="font-size: 24px; font-weight: bold; letter-spacing: 5px;">'
                consonant_html += ' '.join([f'<span style="color: #2196F3; background: #E3F2FD; padding: 8px 12px; margin: 2px; border-radius: 5px; display: inline-block;">{c}</span>' for c in consonants])
                consonant_html += '</div>'
                st.markdown(consonant_html, unsafe_allow_html=True)
            
            with col_v:
                st.markdown("**Vowels:**")
                vowel_html = '<div style="font-size: 24px; font-weight: bold; letter-spacing: 5px;">'
                vowel_html += ' '.join([f'<span style="color: #FF9800; background: #FFF3E0; padding: 8px 12px; margin: 2px; border-radius: 5px; display: inline-block;">{v}</span>' for v in vowels_guessed])
                vowel_html += '</div>'
                st.markdown(vowel_html, unsafe_allow_html=True)
        else:
            st.info("No letters guessed yet")

if __name__ == "__main__":
    main()
