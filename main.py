from ssd1309 import Display
from machine import Pin, SPI
from xglcd_font import XglcdFont
import time
import random

spi = SPI(0, baudrate=14500000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(16), cs=Pin(17), rst=Pin(20))
button = Pin(21, Pin.IN, Pin.PULL_UP)
reset = Pin(22, Pin.IN, Pin.PULL_UP)
bally = XglcdFont('fonts/Bally7x9.c', 7, 9)

class Main:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.frames = 0
        self.player = None
        self.obs = None
        self.player = Dino()
        self.obs = []
        self.end = False
        self.start_time = time.ticks_ms()
        self.frames_until_next_obs = 10

    def environment_specific_logic(self):
        # Used by simulator.
        pass

    def main_game_loop(self):
        while True:
            preframe = time.ticks_ms()
            self.environment_specific_logic()

            if not self.end:
                self.loop()
            else:
                if reset.value() == 0:
                    self.reset()
                    self.end = False

            self.draw()
            time.sleep_ms(16 - time.ticks_diff(time.ticks_ms(), preframe))
        
    def dino_intersects_obstacle(self, dino, obs):
        return display.bitmaps_collide(
            "images/DinoStand1.mono",
            dino.x,
            display.height - dino.img_height - int(dino.y),
            dino.img_width,
            dino.img_height,
            obs.img_path,
            obs.x,
            display.height - obs.img_height,
            obs.img_width,
            obs.img_height
        )
        
    def loop(self):
        self.player.loop()

        self.frames_until_next_obs -= 1
        if self.frames_until_next_obs <= 0:
            new_obs = Obstacle(int(random.uniform(0, len(obstacle_sizes))))
            self.obs.append(new_obs)
            self.frames_until_next_obs = int(max(20, random.uniform(95, 130) - self.player.speed * 10))

        for o in self.obs:
            o.speed = self.player.speed
            if o.is_off_screen():
                self.obs.pop(0)
                self.player.score += 5
                if self.player.score%25 == 0:
                    self.player.speed += 0.25
            o.loop()
            if self.dino_intersects_obstacle(self.player, o):
                self.end = True
                print(self.player.score)
                return

    def draw(self):
        display.clear_buffers()
        self.player.draw()
        for o in self.obs:
            o.draw()
        display.present()
        self.frames += 1
       
class Dino:
    def __init__(self):
        self.score = 0
        self.speed = 2.75
        self.vel_y = 0
        self.acc_y = -0.4
        self.jump_velocity = 6
        self.img_width = 22
        self.img_height = 24
        self.on_ground = True
        self.x = 0
        self.y = 0
        
    def loop(self):
        self.vel_y += self.acc_y
        self.y += self.vel_y

        self.on_ground = self.y <= 0
        if self.on_ground:
            self.y = 0
            self.vel_y = 0

        jump = button.value() == 0
        if jump and self.on_ground:
            self.vel_y = self.jump_velocity
        elif not jump:
            if self.vel_y > 2:
                self.vel_y = 2

    def draw(self):
        if m.end:
            bitmap = "images/DinoDead.mono"
        elif not self.on_ground:
            bitmap = "images/DinoAir.mono"
        elif m.frames % 8 < 4:
            bitmap = "images/DinoStand0.mono"
        else:
            bitmap = "images/DinoStand1.mono"
        display.draw_bitmap(bitmap, 0, display.height - self.img_height - int(self.y), self.img_width, self.img_height)
        
        score_width = bally.measure_text(str(self.score))
        speed_width = bally.measure_text(str(self.speed))
        display.draw_text(display.width - score_width, 0, str(self.score), bally)
        display.draw_text(display.width - speed_width, 17, str(self.speed), bally)

        if m.end:
            game_over_text = "Game Over"
            game_over_width = bally.measure_text(game_over_text)
            display.draw_text(display.width / 2 - game_over_width / 2, 17, game_over_text, bally)

            image_width = 36
            image_height = 32
            display.draw_bitmap("images/GameOver.mono", display.width / 2 - image_width / 2, 28, image_width, image_height)

obstacle_sizes = [
    (24, 25), # 0
    (24, 25), # 1
    (11, 25), # 2
]

class Obstacle:
    def __init__(self, obs_type):
        self.img_path = "images/obs-" + str(obs_type) + ".mono"
        self.img_width, self.img_height = obstacle_sizes[obs_type]
        
        self.x = display.width
        self.y = 0
        self.speed = 1.5
    
    def is_off_screen(self):
        return self.x <= 0 - self.img_width
    
    def loop(self):
        self.x -= self.speed

    def draw(self):
        display.draw_bitmap(self.img_path, int(self.x), display.height - self.img_height, self.img_width, self.img_height)

m = Main()

if __name__ == '__main__':
    m.main_game_loop()
