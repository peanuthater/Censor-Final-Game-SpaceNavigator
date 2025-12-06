# ==========================
#   Game Logic - With High Scores
# ==========================
import time
import random

class GameLogic:
    def __init__(self, hardware, game_ui, high_score_manager):
        self.hardware = hardware
        self.ui = game_ui
        self.hsm = high_score_manager 
        self.current_difficulty = "EASY"
        self.current_score = 0     
        self.ACTIONS = ["TURN_LEFT", "TURN_RIGHT", "PRESS", "TILT_LEFT", "TILT_RIGHT"]
       
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"
        self.CHAR_COUNT = 3 
        
    # ==========================
    #   Action Time per Level
    # ==========================
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
        
    # ==========================
    #   Score Value
    # ==========================
    def get_score_value(self, difficulty):
        if difficulty == "EASY":
            return 1
        elif difficulty == "MEDIUM":
            return 2
        else:  # HARD
            return 3
            
    # ==========================
    #   Wait D2 -> Go to Difficulty
    # ==========================
    def wait_for_start(self):
        boot_time = time.monotonic()
        lock_duration = 1.2
        while True:
            if time.monotonic() - boot_time < lock_duration:
                time.sleep(0.01)
                continue
            if self.hardware.is_encoder_btn_pressed():
                self.hardware.wait_for_button_release()
                self.hardware.encoder_reset()
                return
            time.sleep(0.01)
            
    # ==========================
    #   Difficulty Menu
    # ==========================
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
            
    # ==========================
    #   One Level (Modified for split screens)
    # ==========================
    def play_level(self, difficulty, level):
        actions_count = level
        action_time = self.get_action_time(difficulty, level)
       
        self.ui.show_level_number_only(level)
        time.sleep(1.0) 
      
        self.ui.show_level_intro_details(action_time, actions_count)
        time.sleep(1.0) 
        
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
                    self.ui.show_failure_feedback("Wrong Action!", self.current_score)
                    time.sleep(1.5)
                    return False
                if time.monotonic() - start > action_time:
                    self.ui.show_failure_feedback("Timeout!", self.current_score)
                    time.sleep(1.5)
                    return False
                time.sleep(0.01)
        # Level success: Add score
        score_earned = self.get_score_value(difficulty)
        self.current_score += score_earned

        self.ui.show_level_complete_simple(self.current_score)
        time.sleep(1.5) 
        return True
    
    # ==========================
    #   High Score Initial Entry (New)
    # ==========================
    def enter_initials(self, high_score_index):
       
        initials = ["A", "A", "A"]
        char_index = 0 
        
        char_set_index = 0
        
        self.hardware.encoder_reset()
        
        while char_index < self.CHAR_COUNT:
            current_char = initials[char_index]
            try:
                char_set_index = self.ALPHABET.index(current_char)
            except ValueError:
                char_set_index = 0
            
            self.ui.show_initial_entry("".join(initials), char_index)
            
            while True:
                self.hardware.update_encoder()
                
                if self.hardware.encoder_pos != 0:
                    step = 1 if self.hardware.encoder_pos > 0 else -1
                    char_set_index = (char_set_index + step) % len(self.ALPHABET)
                    initials[char_index] = self.ALPHABET[char_set_index]
                    self.hardware.encoder_reset()
                    self.ui.show_initial_entry("".join(initials), char_index)
                
                if self.hardware.is_encoder_btn_pressed():
                    self.hardware.wait_for_button_release()
                    char_index += 1
                    self.hardware.encoder_reset()
                    break
                    
                time.sleep(0.01)
        
        final_initials = "".join(initials).upper()
        self.hsm.update_initials(high_score_index, final_initials)
        time.sleep(0.5) 
        
    # ==========================
    #   Display Leaderboard (New)
    # ==========================
    def show_leaderboard_loop(self):
        self.hardware.encoder_reset()
        self.ui.show_high_scores(self.hsm.get_scores())
        
        while True:
            if self.hardware.is_encoder_btn_pressed():
                self.hardware.wait_for_button_release()
                return
            time.sleep(0.05)
            
    # ==========================
    #   Restart
    # ==========================
    def wait_for_restart(self):
        self.ui.show_wait_restart()
        while True:
            if self.hardware.is_encoder_btn_pressed():
                self.hardware.wait_for_button_release()
                self.hardware.encoder_reset()
                return
            time.sleep(0.01)
            
    # ==========================
    #   Main Loop (Modified for High Score Flow)
    # ==========================
    def run_game_loop(self):
        self.ui.show_start_screen()
        self.wait_for_start()
        while True:
            self.current_score = 0
            game_ended_naturally = False 
            
            difficulty = self.choose_difficulty()
            
            for level in range(1, 11):
                success = self.play_level(difficulty, level)
                if not success:
                    self.ui.show_game_over(f"Score: {self.current_score}")
                    time.sleep(1.5) 
                    game_ended_naturally = True 
                    break
                if level == 10:
                    self.ui.show_victory(self.current_score)
                    time.sleep(1.5)
                    game_ended_naturally = True 
                    break
            
            if game_ended_naturally:
                high_score_index = self.hsm.check_and_insert_score(self.current_score)
                
                if high_score_index != -1:
                    self.enter_initials(high_score_index)
                
                self.show_leaderboard_loop()

            self.wait_for_restart()
