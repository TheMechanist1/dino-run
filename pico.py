from machine import Pin, SPI
from ssd1309 import Display
import main

spi = SPI(0, baudrate=14500000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(16), cs=Pin(17), rst=Pin(20))
button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)

if __name__ == '__main__':
    main.display = display
    main.button = button
    m = main.Main()
    while True:
        m.update()
        m.render()