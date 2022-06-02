import time

# These will be set later
# See ssd1309.Display
display = None
# See machine.Button
button = None

bally = None

frames = 0

end = False

class Main:
    def __init__(self):
        self.player = Dino()
        self.obs = [Obstacle(0)]
        
    def detectCollision(self, dino, obs):
        return (dino.x < obs.x + obs.imgWidth and dino.x + dino.imgWidth > obs.x and
                dino.y < obs.y + obs.imgHeight and dino.imgHeight + dino.y > obs.y)
        
    def loop(self):
        global end
        self.player.loop()
        for o in self.obs:
            if self.detectCollision(self.player, o):
                print("bruh")
                self.obs.pop(0)
                end = True
                return
            o.speed = self.player.speed
            if o.isOffScreen():
                self.obs.pop(0)
                newOb = Obstacle(int(random.uniform(0,2)))
                newOb.x += random.uniform(0,5) + 30
                self.obs.append(newOb)
            o.loop()

    def draw(self):
        global frames
        display.clear_buffers()
        self.player.draw()
        for o in self.obs:
            o.draw()
        display.present()
        frames += 1
        
class Dino:
    def __init__(self):
        self.score = 0
        self.speed = 1.5
        self.velY = 0
        self.accY = -0.1
        self.imgWidth = 22
        self.imgHeight = 24
        self.x = 0
        self.y = 0
        
    def loop(self):
        self.velY += self.accY
        if ((self.y + self.velY) >= 0):
            self.y += self.velY
        else:
            self.velY = 0
            self.y = 0
        
        if button.value() == 0 and self.velY < 1 and self.y <= 0.1:
            self.velY += 3
        self.score = time.ticks_diff(time.ticks_ms(), startTime)
        if(self.score%10000 <= 16):
            self.speed += 0.25
            print(self.speed)
            
    def draw(self):
        global frames
        if frames%10 < 5:
            display.draw_bitmap("images/DinoStand0.mono", 0, display.height - self.imgHeight - int(self.y), self.imgWidth, self.imgHeight)
        else:
            display.draw_bitmap("images/DinoStand1.mono", 0, display.height - self.imgHeight - int(self.y), self.imgWidth, self.imgHeight)
        
        textWidth = bally.measure_text(str(self.score))
        display.draw_text(display.width - textWidth, 0, str(self.score), bally)
        
        
class Obstacle:
    def __init__(self, obsType):
        if obsType == 0:
            self.imgPath = "images/obs-0.mono"
            self.imgWidth = 24
            self.imgHeight = 25
        elif obsType == 1:
            self.imgPath = "images/obs-1.mono"
            self.imgWidth = 24
            self.imgHeight = 25
        elif obsType == 2:
            self.imgPath = "images/obs-2.mono"
            self.imgWidth = 24
            self.imgHeight = 25
        elif obsType > 2:
            raise Exception("Obstacale Type should be 0-2. You put " + str(obsType))
        else:
            raise Exception("Bro what are you doing?")
        
        self.x = display.width
        self.y = 0
        self.speed = 1.5
    
    def isOffScreen(self):
        return self.x <= 0 - self.imgWidth
    
    def loop(self):
        self.x -= self.speed
        pass

    def draw(self):
        display.draw_bitmap(self.imgPath, int(self.x), display.height - self.imgHeight, self.imgWidth, self.imgHeight)

if __name__ == '__main__':
    from ssd1309 import Display
    from machine import Pin, SPI
    from xglcd_font import XglcdFont
    import random

    spi = SPI(0, baudrate=14500000, sck=Pin(18), mosi=Pin(19))
    display = Display(spi, dc=Pin(16), cs=Pin(17), rst=Pin(20))
    button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
    bally = XglcdFont('fonts/Bally7x9.c', 7, 9)
    startTime = time.ticks_ms()
    
    m = Main()
    while not end:
        preframe = time.ticks_ms()
        m.loop()
        m.draw()
        time.sleep_ms(16 - time.ticks_diff(time.ticks_ms(), preframe))
