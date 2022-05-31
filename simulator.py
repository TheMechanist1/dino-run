import pygame
from PIL import Image
import sys
import main

# https://www.orientdisplay.com/wp-content/uploads/2021/05/AOM12864A0-1.54WW-ANO.pdf
width = 128
height = 64
scale = 5

# TODO: main should be managing framerate on its own because this has to be the same everywhere
framerate = 60

def parse_mono_image(path, width, height):
    with open(path, "rb") as f:
        mono = f.read()
        rgb = []
        current_x = 0
        for i in mono:
            for j in range(8):
                current_x += 1
                if current_x > width:
                    current_x = 0
                    break
                bit = i & (1 << j)
                if bit == 0:
                    rgb.append(0)
                    rgb.append(0)
                    rgb.append(0)
                else:
                    rgb.append(255)
                    rgb.append(255)
                    rgb.append(255)

    image = Image.frombytes('RGB', (width, height), bytes(rgb))
    scaled_width = width * scale
    scaled_height = height * scale
    resized_image = image.resize((scaled_width, scaled_height), resample=Image.NONE)
    return pygame.image.frombuffer(resized_image.tobytes(), (scaled_width, scaled_height), "RGB")

class SimulatedDisplay:
    def __init__(self):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width * scale, height * scale))

    def draw_bitmap(self, path, x, y, width, height):
        image = parse_mono_image(path, width, height)
        self.screen.blit(image, (x * scale, y * scale))

    def present(self):
        pygame.display.flip()

    def clear(self):
        self.screen.fill((0, 0, 0))

class SimulatedButton:
    def __init__(self):
        self.pressed = False

    def value(self):
        # Apparently 0 means pressed
        return 0 if self.pressed else 1

def run():
    pygame.init()

    clock = pygame.time.Clock()

    main.display = SimulatedDisplay()
    main.button = SimulatedButton()
    m = main.Main()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    main.button.pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    main.button.pressed = False

        m.loop()
        m.draw()

        clock.tick(framerate)

if __name__ == '__main__':
    run()
