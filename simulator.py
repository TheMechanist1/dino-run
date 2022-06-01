import pygame
from PIL import Image
import sys
import functools
import game

# Physical specs of the screen we have
# https://www.orientdisplay.com/wp-content/uploads/2021/05/AOM12864A0-1.54WW-ANO.pdf
width = 128
height = 64

scale = 8

# TODO: main should be managing framerate on its own because this has to be the same everywhere
framerate = 60

QUIT_KEYS = [pygame.K_ESCAPE, pygame.K_q]

JUMP_KEYS = [pygame.K_SPACE, pygame.K_UP]

@functools.lru_cache
def parse_mono_image(path, width, height):
    print(f"Loading mono image {path}")

    with open(path, "rb") as f:
        mono = f.read()

        # Each bit in the mono image represents up to 1 pixel of the image
        # 1 is white, 0 is black
        # When a row ends, the rest of the current byte is skipped
        # A 10x4 image might have data like this:
        #   11111111 11000000
        #   00110100 01000000
        #   00111110 00000000
        #   10111101 11000000
        # Notice how the last 6 bits of each row's last byte are empty.

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
        # Make sure to set the caption before actually creating the window to avoid seeing the wrong
        # name for a moment.
        pygame.display.set_caption('Dino Run')
        self.screen = pygame.display.set_mode((width * scale, height * scale))

    def _prepare_frame(self):
        self._times_cleared = 0
        self._timed_presented = 0

    def _end_frame(self):
        if self._times_cleared != 1:
            print(f"Simulator warning: display.clear() called {self._times_cleared} times but it should be called exactly once per frame")
        if self._timed_presented != 1:
            print(f"Simulator warning: display.present() called {self._timed_presented} times but it should be called exactly once per frame")

    def draw_bitmap(self, path, x, y, width, height):
        image = parse_mono_image(path, width, height)
        self.screen.blit(image, (x * scale, y * scale))

    def clear(self):
        self.screen.fill((0, 0, 0))
        self._times_cleared += 1

    def present(self):
        pygame.display.flip()
        self._timed_presented += 1

class SimulatedButton:
    def __init__(self):
        self.pressed = False

    def value(self):
        # Apparently 0 means pressed
        return 0 if self.pressed else 1

def run():
    pygame.init()

    clock = pygame.time.Clock()

    game.display = SimulatedDisplay()
    game.button = SimulatedButton()
    m = game.Main()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in QUIT_KEYS:
                    sys.exit()
                elif event.key in JUMP_KEYS:
                    game.button.pressed = True
            elif event.type == pygame.KEYUP:
                if event.key in JUMP_KEYS:
                    game.button.pressed = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.button.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                game.button.pressed = False

        game.display._prepare_frame()

        m.loop()
        m.draw()

        game.display._end_frame()

        clock.tick(framerate)

if __name__ == '__main__':
    run()
