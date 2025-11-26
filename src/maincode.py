import time
import board
import busio

import displayio
displayio.release_displays() 

i2c = busio.I2C(board.D8, board.D3) 

from game_hardware import Hardware
from game_logic import GameLogic
from game_ui import GameUI

def main():
    hardware = Hardware(i2c)
    
    game_ui = GameUI(hardware)
    game_logic = GameLogic(hardware, game_ui)
    
    while True:
        try:
            game_logic.run_game_loop() 
            
        except Exception as e:
            print(f"Global Exception: {e}")
            game_ui.display_message(["Error occurred", "Restarting..."])
            hardware.set_led_color("RED")
            time.sleep(2)
            hardware.encoder_reset()

if __name__ == "__main__":
    main()
