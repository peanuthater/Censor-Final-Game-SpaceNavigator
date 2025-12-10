# Space Navigator — Embedded Reaction Game (Censor Final Project)
<br>

## Overview
Space Navigator is an interactive, reaction-based embedded game designed using CircuitPython. The system integrates an OLED display, NeoPixel LED ring, ADXL343 accelerometer, and a rotary encoder with push-button input.<br>
Players must respond quickly to on-screen commands—rotating the encoder, pressing the button, or tilting the controller—before time runs out. As the game advances, the difficulty increases through shorter action windows and more demanding sequences.<br>
This project is implemented using a modular architecture with the following components:
1. game_hardware.py — Hardware abstraction layer
2. game_logic.py — Game state machine, scoring, and high-score logic
3. game_ui.py — Rendering engine for all on-screen UI and animations
4. high_score_manager.py — Persistent high-score storage simulator
5. rotary_encoder.py — Low-level quadrature rotary encoder driver
6. maincode.py — Main program entry point
<br>

## Game Mechanics and Flow
### 1. Boot Animation
At startup, an ASCII-style animated character walks across the screen.<br>
This animation is rendered frame-by-frame using a small custom text canvas, providing a lively opening sequence.

### 2. Start Screen
The OLED displays the title screen.<br>
The game begins when the player presses the encoder button.

### 3. Difficulty Selection
Players rotate the encoder to select a difficulty level:<br>
EASY — Longest action window, lowest score per level<br>
MEDIUM — Moderate difficulty<br>
HARD — Faster pace, highest reward<br>
LED colors give visual feedback for each selection.

### 4. Level Structure
The game consists of 10 levels, each containing a number of actions equal to the current level number:<br>
Level 1 → 1 action<br>
Level 2 → 2 actions<br>
…<br>
Level 10 → 10 actions<br>

Each action is randomly selected from:<br>
TURN_LEFT<br>
TURN_RIGHT<br>
PRESS (encoder push button)<br>
TILT_LEFT (detected via accelerometer)<br>
TILT_RIGHT<br>
The allowed reaction time decreases with level progression, determined by a difficulty-based timing function.

### 5. Scoring System
Points awarded per level completion:<br>
EASY → +1<br>
MEDIUM → +2<br>
HARD → +3<br>
The current score is displayed after each level.

### 6. Game Over & Victory Conditions
Incorrect actions or timeouts result in an immediate Game Over.<br>
Completing all ten levels results in Victory.<br>
Both outcomes display a dedicated end screen with the player's final score.

### 7. High Score System (with Initials Entry)
After the game concludes:<br>
The score is compared with the top 3 leaderboard.<br>
If the player qualifies:<br>
A 3-character initials entry interface appears.<br>
Characters cycle through A–Z, digits, and space using the rotary encoder.<br>
Button press confirms each character.<br>
The updated leaderboard is stored using a simulated NVM serialization method.<br>
A formatted high-score table is displayed until the player presses the button.

### 8. Restart Loop
The game waits for the player to press the encoder button, then resets and returns to the start screen.
<br>

## Code Architecture
Project Directory Structure:<br>
1. game_hardware.py
2. game_logic.py
3. game_ui.py
4. high_score_manager.py
5. rotary_encoder.py
6. maincode.py
Each file implements a single responsibility to preserve clarity and maintainability.

### 1. Hardware Module — game_hardware.py
Responsibilities:<br>
Initialize OLED display (SSD1306)<br>
Initialize ADXL343 accelerometer<br>
Manage NeoPixel LED ring (approx. 60 LEDs)<br>
Poll rotary encoder and its push-button<br>
Provide debounced button input<br>
Interpret motion gestures (tilt left/right)<br>
Manage LED color states<br>
Provide uniform hardware API for the game logic module<br>
This module acts as the hardware abstraction layer, ensuring that all other modules remain hardware-agnostic.

### 2. Game Logic Module — game_logic.py
Key responsibilities:<br>
Implements the entire game state machine<br>
Handles difficulty selection, timing, and action scheduling<br>
Executes level progression<br>
Validates player actions against required input<br>
Assigns score based on difficulty<br>
Detects win/lose conditions<br>
Integrates with UI for display updates<br>
Handles initials entry for high-score updates<br>
Coordinates high-score insertion and display<br>
This module is the operational “brain” of the game.

### 3. User Interface Module — game_ui.py
Responsible for everything rendered onto the OLED display:<br>
Boot animation<br>
Start / difficulty / level intro screens<br>
Action prompts<br>
Success and failure feedback<br>
Game Over / Victory screens<br>
High-score table formatting<br>
Animated initials-entry UI<br>
The UI module never makes game decisions—it simply displays the data provided by the logic layer.

### 4. High Score Manager — high_score_manager.py
Features:<br>
Maintains a three-entry leaderboard<br>
Loads default scores<br>
Inserts new scores in descending order<br>
Handles initials updates<br>
Serializes leaderboard to an NVM-like string<br>
Prints simulated save output for evaluation<br>
High scores are stored in internal memory format such as:<br>
18,LYA<br>
16,PNT<br>
11,JOE

### 5. Rotary Encoder Module — rotary_encoder.py
A dedicated low-level driver for reading a mechanical quadrature rotary encoder.<br>
Core functionality:<br>
Reads phase A/B signals from GPIO pins<br>
Converts transitions into rotation steps<br>
Supports debounce and detent resolution<br>
Provides clean, direction-stable increments (+1 or -1)<br>
Fully encapsulates encoder behavior for reuse<br>
This module significantly improves the precision and reliability of user input.

### 6. Main Program — maincode.py
Entry point responsibilities:<br>
Initialize all subsystems (hardware, UI, logic, high-score manager)<br>
Play boot animation once<br>
Enter the main game loop<br>
Recover from unexpected exceptions and restart safely<br>
Ensures stable continuous gameplay.
<br>

## Hardware Components
| Component                                      | Description                 | Purpose                              |
| ---------------------------------------------- | --------------------------- | ------------------------------------ |
| **Microcontroller (CircuitPython-compatible)** | Central processor           | Runs game logic                      |
| **SSD1306 OLED Display (128×64, I²C)**         | Main screen                 | Game UI visuals                      |
| **NeoPixel LED Ring (~60 LEDs)**               | RGB LED effects             | Difficulty and status feedback       |
| **ADXL343 Accelerometer**                      | 3-axis motion detection     | Tilt detection                       |
| **Rotary Encoder + Push Button**               | Rotational and button input | Menu navigation, in-game actions     |
| **Custom 3D-printed Enclosure**                | Physical housing            | Structural protection and ergonomics |

I²C wiring:<br>
SDA → D8<br>
SCL → D3
<br>

## Enclosure Design Rationale
### 1. Ergonomics
Encoder positioned for natural right-handed use<br>
Button offers clear tactile response<br>
Display angled toward the player for readability

### 2. Modular Internal Layout
Top layer: OLED + encoder<br>
Middle: microcontroller board<br>
Bottom: NeoPixel ring and cable routing<br>
Ensures clean internal organization and reduces interference.

### 3. Aesthetic Theme
Inspired by a spacecraft control console:<br>
Circular LED ring resembles a navigation instrument<br>
Matte-black PLA shell gives a sci-fi visual style<br>
LED colors reflect system state (success, failure, difficulty, etc.)

### 4. Durability Considerations
Reinforced encoder mount<br>
Protective bezel for OLED<br>
Venting ports prevent overheating<br>


## Summary
Space Navigator is a fully modular, scalable, and visually engaging reaction game system.<br>
By separating hardware, logic, UI, and input driver modules, the project demonstrates strong engineering practices and is suitable for academic submission, personal projects, and embedded systems prototyping.<br>
Future expansions could include:<br>
1. Sound effects
2. Additional sensor-based actions
3. Larger leaderboard
4. Additional game modes
5. Wireless communication
