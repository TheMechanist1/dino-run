from time import sleep
from machine import Pin, SPI
from ssd1309 import Display

class Main:
    def __init__(self):
        print(d.speed)
        self.spi = SPI(0, baudrate=14500000, sck=Pin(18), mosi=Pin(19))
        self.display = Display(self.spi, dc=Pin(16), cs=Pin(17), rst=Pin(20))
        
    def loop(self):
        pass

    def draw(self):
        self.display.draw_bitmap("images/DinoStand1.mono", 0, self.display.height - 22, 20, 22)
        self.display.present()
        
        self.display.draw_bitmap("images/DinoStand2.mono", 0, self.display.height - 22, 20, 22)
        self.display.present()

class Dino:
    def __init__(self, score, speed):
        self.score = score
        self.speed = speed
        
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

d = Dino(0, 0)

if __name__ == "__main__":
    m = Main();
    while True:
        m.loop()
        m.draw()