# Stub reimplementation of the utime module for the simulator
# https://docs.micropython.org/en/latest/library/time.html

import time

def sleep_ms(ms):
    time.sleep(ms / 1000.0)
