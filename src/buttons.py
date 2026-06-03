from unittest.mock import MagicMock

# インポートガード
try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = MagicMock()


class ControlButton:
    def __init__(self, pin_start, pin_stop, gpio=GPIO):
        self.pin_start = pin_start
        self.pin_stop = pin_stop
        self.gpio = gpio  # ここでモックを保存

        # GPIO定数がない場合のフォールバック（テスト用）
        self.gpio.BCM = getattr(self.gpio, 'BCM', 'BCM')
        self.gpio.IN = getattr(self.gpio, 'IN', 'IN')
        self.gpio.PUD_UP = getattr(self.gpio, 'PUD_UP', 'PUD_UP')
        self.gpio.LOW = 0
        self.gpio.HIGH = 1

        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.pin_start, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.setup(self.pin_stop, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)

        self.last_stop_press = 0

    def get_stop_action(self):
        import time
        # self.gpio を必ず使用する
        if self.gpio.input(self.pin_stop) == self.gpio.LOW:
            start_time = time.time()
            while self.gpio.input(self.pin_stop) == self.gpio.LOW:
                time.sleep(0.1)
                if time.time() - start_time > 3.0:
                    return 'LONG'
            now = time.time()
            if now - self.last_stop_press < 0.5:
                self.last_stop_press = 0
                return 'DOUBLE'
            self.last_stop_press = now
            return 'SINGLE'
        return 'NONE'

    def is_start_pressed(self):
        return self.gpio.input(self.pin_start) == self.gpio.LOW
