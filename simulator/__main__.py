import pygame
pygame.init()

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import micropython_extensions
import pygame
import generate_mono_images
from PIL import Image
import time

import main

scale = 8

QUIT_KEYS = [pygame.K_ESCAPE, pygame.K_q]

RESET_KEYS = [pygame.K_r]

JUMP_KEYS = [pygame.K_SPACE, pygame.K_UP]

def upscale_surface(surface: pygame.Surface, factor: float) -> pygame.Surface:
    width, height = surface.get_size()
    image = Image.frombytes("RGBA", (width, height), pygame.image.tostring(surface, "RGBA"))
    scaled_width = width * factor
    scaled_height = height * factor
    resized_image = image.resize((scaled_width, scaled_height), resample=Image.NONE)
    return pygame.image.frombuffer(resized_image.tobytes(), resized_image.size, resized_image.mode)

def run():
    m = main.Main()

    pygame.display.set_caption('Dino Run')
    width = main.display.width
    height = main.display.height
    screen = pygame.display.set_mode((width * scale, height * scale))

    def present_to_pygame():
        screen.fill((0, 0, 0, 0))
        screen.blit(upscale_surface(main.display.monoFB.surface, scale), (0, 0))
        pygame.display.flip()
    main.display.present = present_to_pygame

    def handle_pygame_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                is_down = event.type == pygame.KEYDOWN
                if event.key in QUIT_KEYS:
                    if is_down:
                        sys.exit()
                elif event.key in JUMP_KEYS:
                    main.button.set_value(0 if is_down else 1)
                elif event.key in RESET_KEYS:
                    main.reset.set_value(0 if is_down else 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main.button.set_value(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                main.button.set_value(1)

    m.environment_specific_logic = handle_pygame_events

    while True:
        m.main_game_loop()

if __name__ == '__main__':
    generate_mono_images.generate()
    run()
