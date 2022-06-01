from time import sleep

# These will be set by either pico.py or simulator.py
# See ssd1309.Display
display = None
# See machine.Button
button = None

class Main:
    def __init__(self):
        self.player = Dino(0, 0, 0)
        
        
    def loop(self):
        self.player.loop()

    def draw(self):
        self.player.draw()
        

class Dino:
    def __init__(self, score, speed, y):
        self.score = score
        self.speed = speed
        self.y = y
        self.velY = y
        self.accY = -0.1
        
    def loop(self):
        self.velY += self.accY
        if ((self.y + self.velY) >= 0):
            self.y += self.velY
            display.clear()
        else:
            self.velY = 0
            self.y = 0
        
        if button.value() == 0 and self.velY < 1 and self.y <= 0.1:
            self.velY += 3
            print(self.y)
            
    
    def draw(self):
        display.draw_bitmap("images/DinoStand1.mono", 0, display.height - 22 - int(self.y), 20, 22)
        display.present()
        
        display.draw_bitmap("images/DinoStand2.mono", 0, display.height - 22 - int(self.y), 20, 22)
        display.present()
        
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def getX():
        return self.x
    
    def getY():
        return self.y
