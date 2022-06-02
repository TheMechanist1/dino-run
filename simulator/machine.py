# Stub reimplementation of the machine module for the simulator
# https://docs.micropython.org/en/latest/library/machine.html

class Pin:
    OUT = 1
    IN = 2

    PULL_UP = 3

    def __init__(self, id, mode=- 1, pull=- 1):
        self.id = id
        self._value = 1

    def init(mode=- 1, pull=- 1, *, value=None, drive=0, alt=- 1):
        pass

    def set_value(self, value):
        self._value = value

    def __call__(self, value):
        self.set_value(value)

    def value(self):
        return self._value

class SPI:
    def __init__(self, id, baudrate, sck, mosi):
        self.id = id
        self.baudrate = baudrate
        self.sck = sck
        self.mosi = mosi

    def write(self, bytes):
        pass
