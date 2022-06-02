import time

# These will be set later
# See ssd1309.Display
display = None
# See machine.Button
button = None

bally = None

frames = 0

class Main:
    def __init__(self):
        self.player = Dino()
        self.obs = Obstacle(0, 0)
        
    def loop(self):
        self.player.loop()
        self.obs.loop()

    def draw(self):
        global frames
        display.clear_buffers()
        self.player.draw()
        self.obs.draw()
        display.present()
        frames += 1
        
class Dino:
    def __init__(self):
        self.score = 0
        self.speed = 0
        self.y = 0
        self.velY = 0
        self.accY = -0.1
        
    def loop(self):
        self.velY += self.accY
        if ((self.y + self.velY) >= 0):
            self.y += self.velY
        else:
            self.velY = 0
            self.y = 0
        
        if button.value() == 0 and self.velY < 1 and self.y <= 0.1:
            self.velY += 3
            self.score += 1
            
    def draw(self):
        global frames
        if frames%10 < 5:
            display.draw_bitmap("images/DinoStand0.mono", 0, display.height - 24 - int(self.y), 22, 24)
        else:
            display.draw_bitmap("images/DinoStand1.mono", 0, display.height - 24 - int(self.y), 22, 24)
        
        textWidth = bally.measure_text(str(self.score))
        display.draw_text(display.width - textWidth, 0, str(self.score), bally)
        
        
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def loop(self):
        pass

    def draw(self):
        display.draw_bitmap("images/obs-0.mono", 0, display.height - 33 - int(self.y), 32, 33)

if __name__ == '__main__':
    from ssd1309 import Display
    from machine import Pin, SPI
    from xglcd_font import XglcdFont

    spi = SPI(0, baudrate=14500000, sck=Pin(18), mosi=Pin(19))
    display = Display(spi, dc=Pin(16), cs=Pin(17), rst=Pin(20))
    button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
    bally = XglcdFont('fonts/Bally7x9.c', 7, 9)

    m = Main()
    while True:
        preframe = time.ticks_ms()
        m.loop()
        m.draw()
        time.sleep_ms(16 - time.ticks_diff(time.ticks_ms(), preframe))
