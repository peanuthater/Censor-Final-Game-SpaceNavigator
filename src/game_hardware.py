# ==========================
#   Hardware Control Module
#   D7 Removed Version
# ==========================
import time
import board
import digitalio
import neopixel
from rotary_encoder import RotaryEncoder


class Hardware:
    NEOPIXEL_COUNT = 60 

    def __init__(self, i2c):
        print("Initializing hardware...")

        self.i2c = i2c

        self.setup_displays()
        self.setup_sensors()
        self.setup_buttons()
        self.setup_encoder()

        self.encoder_pos = 0
        
        # DEBUG: Print initial acceleration values
        x, y, z = self.accel.acceleration
        print(f"Initial Acceleration: X={x:.2f}, Y={y:.2f}, Z={z:.2f}") 

        print("Hardware setup complete")

    # ==========================
    #   OLED Display (Modified for Centering)
    # ==========================
    def setup_displays(self):
        import displayio
        import terminalio
        from adafruit_display_text import label
        import adafruit_displayio_ssd1306
        import i2cdisplaybus

        displayio.release_displays()

        display_bus = i2cdisplaybus.I2CDisplayBus(self.i2c, device_address=0x3C)
        self.display = adafruit_displayio_ssd1306.SSD1306(
            display_bus, width=128, height=64
        )

        self.main_group = displayio.Group()
        self.display.root_group = self.main_group

        # Set up text layer for proper centering across the display
        self.text_layer = label.Label(
            terminalio.FONT, 
            text="", 
            anchor_point=(0.5, 0.5),     # Center horizontally and vertically
            anchored_position=(64, 32)   # Center position (128/2, 64/2)
        )
        self.main_group.append(self.text_layer)

    # ==========================
    #   Accelerometer + LED
    # ==========================
    def setup_sensors(self):
        import adafruit_adxl34x

        self.accel = adafruit_adxl34x.ADXL343(self.i2c)
        self.pixel = neopixel.NeoPixel(
            board.D9, 
            self.NEOPIXEL_COUNT, 
            brightness=0.5,
            auto_write=True 
        )

    # ==========================
    #   Only ONE Button (D2)
    # ==========================
    def setup_buttons(self):
        self.encoder_btn = digitalio.DigitalInOut(board.D2)
        self.encoder_btn.direction = digitalio.Direction.INPUT
        self.encoder_btn.pull = digitalio.Pull.UP

        now = time.monotonic()
        self._encoder_last_time = now
        self.button_delay = 0.08  # 80ms debounce

    def is_encoder_btn_pressed(self):
        now = time.monotonic()
        if (not self.encoder_btn.value) and (
            now - self._encoder_last_time > self.button_delay
        ):
            self._encoder_last_time = now
            return True
        return False

    def wait_for_button_release(self):
        while not self.encoder_btn.value:
            time.sleep(0.03)

    # ==========================
    #   Encoder
    # ==========================
    def setup_encoder(self):
        self.encoder = RotaryEncoder(
            board.D0, board.D1, debounce_ms=3, pulses_per_detent=3
        )
        self.encoder_pos = 0

    def update_encoder(self):
        if self.encoder.update():
            self.encoder_pos += self.encoder.position
            self.encoder.position = 0

    def encoder_reset(self):
        self.encoder_pos = 0
        self.encoder.position = 0

    # ==========================
    #   LED
    # ==========================
    def set_led_color(self, state):
        colors = {
            "OFF": (0, 0, 0),
            "GREEN": (0, 255, 0),
            "RED": (255, 0, 0),
            "YELLOW": (255, 255, 0),
            "CYAN": (0, 255, 255),
            "BLUE": (0, 0, 255),
            "PURPLE": (150, 0, 120),
        }
        color = colors.get(state, (0, 0, 0))
        self.pixel.fill(color)

    # ==========================
    #   Motion Detection
    # ==========================
    def detect_action(self):
        self.update_encoder()

        if self.encoder_pos > 0:
            return "TURN_RIGHT"
        if self.encoder_pos < 0:
            return "TURN_LEFT"

        x, y, z = self.accel.acceleration
        
        if y < -3.0:
            return "TILT_LEFT"
        if y > 3.0:
            return "TILT_RIGHT"

        return None
