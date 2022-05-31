import pygame
import sys
import main

pygame.init()

# https://www.orientdisplay.com/wp-content/uploads/2021/05/AOM12864A0-1.54WW-ANO.pdf
width = 128
height = 64
scale = 5

def parse_mono_image(path):
    with open(path, "rb") as f:
        print(f.read())

class SimulatedDisplay:
    def __init__(self):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width * scale, height * scale))

    def draw_bitmap(self, path, x, y, width, height):
        pass

    def present(self):
        pygame.display.flip()

    def clear(self):
        self.screen.fill((0, 0, 0))

class SimulatedButton:
    def __init__(self):
        pass

    def value(self):
        return 0

def run():
    main.display = SimulatedDisplay()
    main.button = SimulatedButton()
    m = main.Main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        m.loop()
        m.draw()

if __name__ == '__main__':
    run()
