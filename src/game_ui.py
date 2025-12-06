# ==========================
#   User Interface Module - FINAL Version
#   Includes: Boot animation, High Score UI
# ==========================
import time
class GameUI:
    def __init__(self, hardware):
        self.hardware = hardware
        
    # ==========================
    #   Boot Animation (Temporarily uses left alignment for movement)
    # ==========================
    def play_boot_animation(self):
        WIDTH = 16 
        HEIGHT = 6
        # Temporarily set the text layer to top-left alignment (0, 0) for the animation
        self.hardware.text_layer.anchor_point = (0.0, 0.0)
        self.hardware.text_layer.anchored_position = (0, 0)
        # Character jump action frames (Height <= 6 lines)
        FRAMES = [
            [  # Frame 0: Standing
                "",
                "   (^_^)",
                "   / | \\",
                "    / \\",
                "",
                ""
            ],
            [  # Frame 1: Left leg raised
                "",
                "   (^_^)",
                "   / | \\",
                "   _/ \\",
                "",
                ""
            ],
            [  # Frame 2: Right leg raised
                "",
                "   (^_^)",
                "   / | \\",
                "    \\_\\",
                "",
                ""
            ],
            [  # Frame 3: Body tilted
                "",
                " ( ^_^ )",
                "    \\|/",
                "    / \\",
                "",
                ""
            ],
        ]
        character_width = 9 
        start_x = -character_width
        end_x = WIDTH + character_width 
        step = 0
        for x in range(start_x, end_x):
            frame_index = (step // 2) % len(FRAMES)
            person = FRAMES[frame_index]
            step += 1
            canvas = [" " * WIDTH for _ in range(HEIGHT)]
            canvas = [list(r) for r in canvas]
            for row_i in range(6):
                line = person[row_i]
                for col_i in range(len(line)):
                    px = x + col_i
                    py = row_i
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        ch = line[col_i]
                        if ch != " ":
                            canvas[py][px] = ch
            final_frame = ["".join(r) for r in canvas]
            self.hardware.text_layer.text = "\n".join(final_frame)
            time.sleep(0.01) 
        # Clear screen
        self.hardware.text_layer.text = ""
        time.sleep(0.1)
        # Restore text layer to center alignment for game UI
        self.hardware.text_layer.anchor_point = (0.5, 0.5)
        self.hardware.text_layer.anchored_position = (64, 32)
        
    # ======================
    #   Generic Text Display (Relies on hardware for centering)
    # ======================
    def display_message(self, lines):
        self.hardware.text_layer.text = "\n".join(lines)
        
    # ======================
    #   Start Screen
    # ======================
    def show_start_screen(self):
        self.hardware.set_led_color("OFF")
        self.display_message([
            "Space_Navigator",
            "",
            "Press to Play!",
            ""
        ])
        
    # ======================
    #   Difficulty Menu
    # ======================
    def show_difficulty_menu(self, current_option_index):
        options = ["EASY", "MEDIUM", "HARD"]
        current_option = options[current_option_index]
        self.display_message([
            "Select Difficulty",
            "> " + current_option,
            "",
            ""
        ])
        if current_option == "EASY":
            self.hardware.set_led_color("YELLOW")
        elif current_option == "MEDIUM":
            self.hardware.set_led_color("CYAN")
        else:
            self.hardware.set_led_color("BLUE")
            
    # ======================
    #   Level Intro Page 1 (Only Level Number) - NEW
    # ======================
    def show_level_number_only(self, level):
        self.display_message([
            "",
            f"Level {level}",
            "",
            ""
        ])
        self.hardware.set_led_color("GREEN")
        
    # ======================
    #   Level Intro Page 2 (Details) - NEW
    # ======================
    def show_level_intro_details(self, total_time, actions_required):
        self.display_message([
            "",
            f"Time: {total_time:.1f}s",
            f"Actions: {actions_required}",
            ""
        ])
        self.hardware.set_led_color("GREEN")
        
    # ======================
    #   Game Screen
    # ======================
    def show_game_screen(self, level, completed, actions_required, required_action):
        step_text = f"{completed+1}/{actions_required}"
        action_text = required_action
        self.display_message([
            f"Level {level}",
            step_text,
            action_text,
            ""
        ])
        self.hardware.set_led_color("PURPLE")
        
    # ======================
    #   Feedback
    # ======================
    def show_success_feedback(self):
        self.display_message([
            "CORRECT!",
            "",
            "",
            ""
        ])
        self.hardware.set_led_color("GREEN")
    def show_failure_feedback(self, message, score):
        self.display_message([
            "FAIL!",
            message,
            f"Score: {score}",
            ""
        ])
        self.hardware.set_led_color("RED")
        
    # ======================
    #   Level Complete (Simplified) - NEW
    # ======================
    def show_level_complete_simple(self, current_score):
        self.display_message([
            "Level Complete!",
            "",
            f"Score: {current_score}",
            ""
        ])
        self.hardware.set_led_color("GREEN")
        
    # ======================
    #   Game Over
    # ======================
    def show_game_over(self, message):
        self.display_message([
            "GAME OVER!",
            "",
            message,
            ""
        ])
        self.hardware.set_led_color("RED")
        
    # ======================
    #   Victory
    # ======================
    def show_victory(self, score):
        self.display_message([
            "YOU WIN!!",
            "Amazing!",
            f"Final Score: {score}",
            ""
        ])
        self.hardware.set_led_color("GREEN")
        
    # ======================
    #   Restart Prompt
    # ======================
    def show_wait_restart(self):
        self.display_message([
            "Press button",
            "to restart",
            "",
            ""
        ])
        
    # ======================
    #   High Score Display (New)
    # ======================
    def show_high_scores(self, scores):
       
        line1 = f"1. {scores[0]['initials']:<3} {scores[0]['score']:>5}"
        line2 = f"2. {scores[1]['initials']:<3} {scores[1]['score']:>5}"
        line3 = f"3. {scores[2]['initials']:<3} {scores[2]['score']:>5}"
        
        self.display_message([
            "High Scores:",
            line1,
            line2,
            line3,
        ])
        self.hardware.set_led_color("CYAN")
        
    # ======================
    #   Initial Entry (New)
    # ======================
    def show_initial_entry(self, current_initials, current_char_index):
   
        display_initials = list(current_initials)
        if current_char_index < len(display_initials):
            display_initials[current_char_index] = '_'
            
        initials_line = "".join(display_initials)
        
        self.display_message([
            "NEW HIGH SCORE!",
            "",
            f"Enter Initials: {initials_line}",
            "Press to Confirm",
        ])
        self.hardware.set_led_color("YELLOW")
