import time

class GameUI:
    def __init__(self, hardware):
        self.hardware = hardware
    
    def display_message(self, lines):
        self.hardware.text_layer.text = "\n".join(lines)

    def show_start_screen(self):
        self.hardware.set_led_color("OFF")
        self.display_message([
            "Space_Navigator :)", 
            "",
            "Press to Play!",
            ""
        ])

    def show_difficulty_menu(self, current_option_index):
        options = ["EASY", "MEDIUM", "HARD"]
        current_option = options[current_option_index]
        
        self.display_message([
            "Select Difficulty:",
            ("> " + current_option).center(16),
            "",
            ""
        ])
        
        if current_option == "EASY":
            self.hardware.set_led_color("YELLOW")
        elif current_option == "MEDIUM":
            self.hardware.set_led_color("CYAN")
        else:
            self.hardware.set_led_color("BLUE")

    def show_level_intro(self, difficulty, level, actions_required, total_time):
        self.display_message([
            f"{difficulty} - Level {level}",
            f"Actions: {actions_required}",
            f"Time: {total_time:.1f}s",
            ""
        ])
        self.hardware.set_led_color("GREEN")

    def show_game_screen(self, level, completed, actions_required, required_action):
        step_text = f"{completed+1}/{actions_required}".center(16)
        action_text = required_action.center(16)

        self.display_message([
            f"Level {level}",
            step_text,
            action_text,
            ""
        ])
        self.hardware.set_led_color("PURPLE")

    def show_success_feedback(self):
        self.display_message([
            "   CORRECT!   ",
            "",
            "",
            ""
        ])
        self.hardware.set_led_color("GREEN")

    def show_failure_feedback(self, message):
        self.display_message([
            "    FAIL!     ",
            message.center(16),
            "",
            ""
        ])
        self.hardware.set_led_color("RED")

    def show_level_complete(self, next_level):
        self.display_message([
            "Level Complete!",
            f"Next: {next_level}",
            "",
            ""
        ])
        self.hardware.set_led_color("GREEN")

    def show_game_over(self, message):
        self.display_message([
            "  GAME OVER!  ",
            message.center(16),
            "",
            ""
        ])
        self.hardware.set_led_color("RED")

    def show_victory(self):
        self.display_message([
            "   YOU WIN!!  ",
            "   Amazing!   ",
            "",
            ""
        ])
        self.hardware.set_led_color("GREEN")

    def show_wait_restart(self):
        self.display_message([
            "Press any button",
            "   to restart   ",
            "",
            ""
        ])
