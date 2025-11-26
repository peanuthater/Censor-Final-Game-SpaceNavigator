import time
import digitalio

class RotaryEncoder:
    def __init__(self, pin_a, pin_b, debounce_ms=3, pulses_per_detent=3):
        self.a = digitalio.DigitalInOut(pin_a)
        self.a.direction = digitalio.Direction.INPUT
        self.a.pull = digitalio.Pull.UP

        self.b = digitalio.DigitalInOut(pin_b)
        self.b.direction = digitalio.Direction.INPUT
        self.b.pull = digitalio.Pull.UP

        self.state = (self.a.value << 1) | self.b.value
        self.position = 0

        self._pulse_count = 0
        self.pulses_per_detent = pulses_per_detent

        self.last_time = time.monotonic()
        self.debounce = debounce_ms / 1000

        self.transitions = {
            (0, 1): +1, (1, 3): +1, (3, 2): +1, (2, 0): +1,
            (0, 2): -1, (2, 3): -1, (3, 1): -1, (1, 0): -1
        }

    def update(self):
        new_state = (self.a.value << 1) | self.b.value

        if new_state != self.state:
            now = time.monotonic()

            if now - self.last_time > self.debounce:
                step = self.transitions.get((self.state, new_state), 0)
                self._pulse_count += step

                if abs(self._pulse_count) >= self.pulses_per_detent:
                    self.position += 1 if self._pulse_count > 0 else -1
                    self._pulse_count = 0
                    self.state = new_state
                    self.last_time = now
                    return True

                self.state = new_state
                self.last_time = now

        return False
