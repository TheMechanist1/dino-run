from ssd1309 import Display
from machine import Pin, SPI
from xglcd_font import XglcdFont
import time
import random

spi = SPI(0, baudrate=14500000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(16), cs=Pin(17), rst=Pin(20))
button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
reset = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
bally = XglcdFont('fonts/Bally7x9.c', 7, 9)

frames = 0

class Main:
    def __init__(self):
        self.player = Dino()
        self.obs = [Obstacle(0)]
        self.end = False
        self.start_time = time.ticks_ms()
        
        
    def reset(self):
        self.player = None
        self.obs = None
        self.player = Dino()
        self.obs = [Obstacle(0)]
        self.end = False
        self.start_time = time.ticks_ms()
    
    def main_game_loop(self):
        while self.end != True:
            preframe = time.ticks_ms()
            self.loop()
            self.draw()
            time.sleep_ms(16 - time.ticks_diff(time.ticks_ms(), preframe))
            
        if(reset.value() == 0):
            self.reset()
            self.end = False
        
    def detect_collision(self, dino, obs):
        return (dino.x < obs.x + obs.img_width and dino.x + dino.img_width > obs.x and
                dino.y < obs.y + obs.img_height and dino.img_height + dino.y > obs.y)
        
    def loop(self):
        self.player.loop()
        self.player.score = time.ticks_diff(time.ticks_ms(), self.start_time)
        for o in self.obs:
            if self.detect_collision(self.player, o):
                print("bruh")
                self.obs.pop(0)
                self.end = True
                return
            o.speed = self.player.speed
            if o.isOffScreen():
                self.obs.pop(0)
                new_obs = Obstacle(int(random.uniform(0,2)))
                new_obs.x += random.uniform(0,5) + 30
                self.obs.append(new_obs)
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
        self.vel_y = 0
        self.acc_y = -0.1
        self.img_width = 22
        self.img_height = 24
        self.x = 0
        self.y = 0
        
    def loop(self):
        self.vel_y += self.acc_y
        if ((self.y + self.vel_y) >= 0):
            self.y += self.vel_y
        else:
            self.vel_y = 0
            self.y = 0
        
        if button.value() == 0 and self.vel_y < 1 and self.y <= 0.1:
            self.vel_y += 3
        
        if(self.score%10000 <= 16):
            self.speed += 0.25
            print(self.speed)
            
    def draw(self):
        global frames
        if frames%10 < 5:
            display.draw_bitmap("images/DinoStand0.mono", 0, display.height - self.img_height - int(self.y), self.img_width, self.img_height)
        else:
            display.draw_bitmap("images/DinoStand1.mono", 0, display.height - self.img_height - int(self.y), self.img_width, self.img_height)
        
        score_width = bally.measure_text(str(self.score))
        speed_width = bally.measure_text(str(self.speed))
        display.draw_text(display.width - score_width, 0, str(self.score), bally)
        display.draw_text(display.width - speed_width, 17, str(self.speed), bally)
        
class Obstacle:
    def __init__(self, obs_type):
        if obs_type == 0:
            self.img_path = "images/obs-0.mono"
            self.img_width = 24
            self.img_height = 25
        elif obs_type == 1:
            self.img_path = "images/obs-1.mono"
            self.img_width = 24
            self.img_height = 25
        elif obs_type == 2:
            self.img_path = "images/obs-2.mono"
            self.img_width = 24
            self.img_height = 25
        elif obs_type > 2:
            raise Exception("Obstacale Type should be 0-2. You put " + str(obs_type))
        else:
            raise Exception("Bro what are you doing?")
        
        self.x = display.width
        self.y = 0
        self.speed = 1.5
    
    def isOffScreen(self):
        return self.x <= 0 - self.img_width
    
    def loop(self):
        self.x -= self.speed

    def draw(self):
        display.draw_bitmap(self.img_path, int(self.x), display.height - self.img_height, self.img_width, self.img_height)

if __name__ == '__main__':
    m = Main()
    while True:
        m.main_game_loop()
