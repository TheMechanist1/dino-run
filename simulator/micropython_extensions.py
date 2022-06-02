# Implement MicroPython time APIs
# https://docs.micropython.org/en/latest/library/time.html
import time

def ticks_diff(a, b):
    return b - a

def ticks_ms():
    return time.time() / 1000

def sleep_ms(ms):
    time.sleep(ms / 1000)

time.ticks_diff = ticks_diff
time.ticks_ms = ticks_ms
time.sleep_ms = sleep_ms
