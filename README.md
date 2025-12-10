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
The OLED displays the title screen.
The game begins when the player presses the encoder button.

### 3. Difficulty Selection
Players rotate the encoder to select a difficulty level:
EASY — Longest action window, lowest score per level
MEDIUM — Moderate difficulty
HARD — Faster pace, highest reward
LED colors give visual feedback for each selection.

### 4. Level Structure
The game consists of 10 levels, each containing a number of actions equal to the current level number:
Level 1 → 1 action
Level 2 → 2 actions
…
Level 10 → 10 actions

Each action is randomly selected from:
TURN_LEFT
TURN_RIGHT
PRESS (encoder push button)
TILT_LEFT (detected via accelerometer)
TILT_RIGHT
The allowed reaction time decreases with level progression, determined by a difficulty-based timing function.

### 5. Scoring System
Points awarded per level completion:
EASY → +1
MEDIUM → +2
HARD → +3
The current score is displayed after each level.

### 6. Game Over & Victory Conditions
Incorrect actions or timeouts result in an immediate Game Over.
Completing all ten levels results in Victory.
Both outcomes display a dedicated end screen with the player's final score.

### 7. High Score System (with Initials Entry)
After the game concludes:
The score is compared with the top 3 leaderboard.
If the player qualifies:
A 3-character initials entry interface appears.
Characters cycle through A–Z, digits, and space using the rotary encoder.
Button press confirms each character.
The updated leaderboard is stored using a simulated NVM serialization method.
A formatted high-score table is displayed until the player presses the button.

### 8. Restart Loop
The game waits for the player to press the encoder button, then resets and returns to the start screen.


## Code Architecture
Project Directory Structure:
1. game_hardware.py
2. game_logic.py
3. game_ui.py
4. high_score_manager.py
5. rotary_encoder.py
6. maincode.py
Each file implements a single responsibility to preserve clarity and maintainability.

### 1. Hardware Module — game_hardware.py
Responsibilities:
Initialize OLED display (SSD1306)
Initialize ADXL343 accelerometer
Manage NeoPixel LED ring (approx. 60 LEDs)
Poll rotary encoder and its push-button
Provide debounced button input
Interpret motion gestures (tilt left/right)
Manage LED color states
Provide uniform hardware API for the game logic module
This module acts as the hardware abstraction layer, ensuring that all other modules remain hardware-agnostic.

### 2. Game Logic Module — game_logic.py
Key responsibilities:
Implements the entire game state machine
Handles difficulty selection, timing, and action scheduling
Executes level progression
Validates player actions against required input
Assigns score based on difficulty
Detects win/lose conditions
Integrates with UI for display updates
Handles initials entry for high-score updates
Coordinates high-score insertion and display
This module is the operational “brain” of the game.

### 3. User Interface Module — game_ui.py
Responsible for everything rendered onto the OLED display:
Boot animation
Start / difficulty / level intro screens
Action prompts
Success and failure feedback
Game Over / Victory screens
High-score table formatting
Animated initials-entry UI
The UI module never makes game decisions—it simply displays the data provided by the logic layer.

### 4. High Score Manager — high_score_manager.py
Features:
Maintains a three-entry leaderboard
Loads default scores
Inserts new scores in descending order
Handles initials updates
Serializes leaderboard to an NVM-like string
Prints simulated save output for evaluation
High scores are stored in internal memory format such as:
18,LYA
16,PNT
11,JOE

### 5. Rotary Encoder Module — rotary_encoder.py
A dedicated low-level driver for reading a mechanical quadrature rotary encoder.
Core functionality:
Reads phase A/B signals from GPIO pins
Converts transitions into rotation steps
Supports debounce and detent resolution
Provides clean, direction-stable increments (+1 or -1)
Fully encapsulates encoder behavior for reuse
This module significantly improves the precision and reliability of user input.

### 6. Main Program — maincode.py
Entry point responsibilities:
Initialize all subsystems (hardware, UI, logic, high-score manager)
Play boot animation once
Enter the main game loop
Recover from unexpected exceptions and restart safely
Ensures stable continuous gameplay.


## Hardware Components
| Component                                      | Description                 | Purpose                              |
| ---------------------------------------------- | --------------------------- | ------------------------------------ |
| **Microcontroller (CircuitPython-compatible)** | Central processor           | Runs game logic                      |
| **SSD1306 OLED Display (128×64, I²C)**         | Main screen                 | Game UI visuals                      |
| **NeoPixel LED Ring (~60 LEDs)**               | RGB LED effects             | Difficulty and status feedback       |
| **ADXL343 Accelerometer**                      | 3-axis motion detection     | Tilt detection                       |
| **Rotary Encoder + Push Button**               | Rotational and button input | Menu navigation, in-game actions     |
| **Custom 3D-printed Enclosure**                | Physical housing            | Structural protection and ergonomics |

I²C wiring:
SDA → D8
SCL → D3


## Enclosure Design Rationale
### 1. Ergonomics
Encoder positioned for natural right-handed use
Button offers clear tactile response
Display angled toward the player for readability

### 2. Modular Internal Layout
Top layer: OLED + encoder
Middle: microcontroller board
Bottom: NeoPixel ring and cable routing
Ensures clean internal organization and reduces interference.

### 3. Aesthetic Theme
Inspired by a spacecraft control console:
Circular LED ring resembles a navigation instrument
Matte-black PLA shell gives a sci-fi visual style
LED colors reflect system state (success, failure, difficulty, etc.)

### 4. Durability Considerations
Reinforced encoder mount
Protective bezel for OLED
Venting ports prevent overheating


## Summary
Space Navigator is a fully modular, scalable, and visually engaging reaction game system.
By separating hardware, logic, UI, and input driver modules, the project demonstrates strong engineering practices and is suitable for academic submission, personal projects, and embedded systems prototyping.
Future expansions could include:
1. Sound effects
2. Additional sensor-based actions
3. Larger leaderboard
4. Additional game modes
5. Wireless communication
