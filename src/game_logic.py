import time
import random

class GameLogic:
    def __init__(self, hardware, game_ui):
        self.hardware = hardware
        self.ui = game_ui

        self.current_difficulty = "EASY"
        self.ACTIONS = ["TURN_LEFT", "TURN_RIGHT", "PRESS", "TILT_LEFT", "TILT_RIGHT"]

    def get_action_time(self, difficulty, level):
        if difficulty == "EASY":
            start_t = 1.5
            end_t   = 1.1
        elif difficulty == "MEDIUM":
            start_t = 1.6
            end_t   = 0.8
        else:
            start_t = 1.2
            end_t   = 0.5

        ratio = (level - 1) / 9
        return start_t + (end_t - start_t) * ratio

    def wait_for_start(self):
        boot_time = time.monotonic()
        lock_duration = 1.2  

        while True:
            self.hardware.update_encoder()

            if time.monotonic() - boot_time < lock_duration:
                time.sleep(0.01)
                continue

            if self.hardware.is_restart_pressed():
                self.hardware.wait_for_button_release()
                self.hardware.encoder_reset()
                return "DIFFICULTY"

            if self.hardware.is_encoder_btn_pressed():
                self.hardware.wait_for_button_release()
                self.hardware.encoder_reset()
                return "START"

            time.sleep(0.01)

    def choose_difficulty(self):
        options = ["EASY", "MEDIUM", "HARD"]
        index = options.index(self.current_difficulty)

        self.ui.show_difficulty_menu(index)
        self.hardware.encoder_reset()

        while True:
            self.hardware.update_encoder()

            if self.hardware.encoder_pos != 0:
                step = 1 if self.hardware.encoder_pos > 0 else -1
                index = (index + step) % len(options)

                self.hardware.encoder_reset()
                self.ui.show_difficulty_menu(index)

            if self.hardware.is_encoder_btn_pressed():
                self.hardware.wait_for_button_release()
                self.current_difficulty = options[index]
                self.hardware.encoder_reset()
                return self.current_difficulty

            time.sleep(0.01)

    def play_level(self, difficulty, level):
        actions_count = level
        action_time = self.get_action_time(difficulty, level)

        self.ui.show_level_intro(difficulty, level, actions_count, action_time)
        time.sleep(1)

        for i in range(actions_count):

            required_action = random.choice(self.ACTIONS)

            self.ui.show_game_screen(level, i, actions_count, required_action)
            start = time.monotonic()

            while True:
                detected = self.hardware.detect_action()

                if self.hardware.is_encoder_btn_pressed():
                    detected = "PRESS"
                    self.hardware.wait_for_button_release()

                if detected == required_action:
                    self.ui.show_success_feedback()
                    self.hardware.encoder_reset()
                    time.sleep(0.4)
                    break

                if detected is not None and detected != required_action:
                    self.ui.show_failure_feedback("Wrong Action!")
                    time.sleep(1.5)
                    return False

                if time.monotonic() - start > action_time:
                    self.ui.show_failure_feedback("Timeout!")
                    time.sleep(1.5)
                    return False

                time.sleep(0.01)

        self.ui.show_level_complete(level + 1)
        time.sleep(1)
        return True

    def wait_for_restart(self):
        self.ui.show_wait_restart()

        while True:
            if self.hardware.is_restart_pressed() or self.hardware.is_encoder_btn_pressed():
                self.hardware.wait_for_button_release()  
                self.hardware.encoder_reset()
                return

            time.sleep(0.01)

    def run_game_loop(self):
        while True:
         
            self.ui.show_start_screen()

            next_action = self.wait_for_start()

            if next_action == "DIFFICULTY":
                self.current_difficulty = self.choose_difficulty()

            difficulty = self.current_difficulty

            for level in range(1, 11):
                success = self.play_level(difficulty, level)

                if not success:
                    self.wait_for_restart()
                    break

                if level == 10:
                    self.ui.show_victory()
                    self.wait_for_restart()
                    break
