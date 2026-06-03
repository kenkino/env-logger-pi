import time
import smbus2


class AQM1602:
    def __init__(self, config):
        self.bus = smbus2.SMBus(config['bus_number'])
        self.addr = config['i2c_address']
        self.last_line1 = None
        self.last_line2 = None
        self.init_display()

    def _command(self, code):
        self.bus.write_byte_data(self.addr, 0x00, code)
        time.sleep(0.05)

    def init_display(self):
        cmds = [0x38, 0x39, 0x14, 0x73, 0x56, 0x6c, 0x38, 0x01, 0x0f]
        for cmd in cmds:
            self._command(cmd)

    def display(self, line1, line2, force=False):
        if not force and (line1 == self.last_line1 and line2 == self.last_line2):
            return

        self._command(0x80)
        self._write_string(line1)
        self._command(0xC0)
        self._write_string(line2)

        self.last_line1, self.last_line2 = line1, line2

    def _write_string(self, message):
        data = [ord(c) for c in message]
        self.bus.write_i2c_block_data(self.addr, 0x40, data)
