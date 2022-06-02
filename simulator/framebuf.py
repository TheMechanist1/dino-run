# Stub reimplementation of the framebuf module for the simulator
# https://docs.micropython.org/en/latest/library/framebuf.html

import pygame
from log import print_warning

GS8 = 1
MONO_HLSB = 2
MONO_HMSB = 3
MONO_VLSB = 4

def parse_mono_hmsb(hmsb_data: bytearray, width: int, height: int) -> pygame.Surface:
    # Each bit in the mono image represents up to 1 pixel of the image
    # 1 is white, 0 is black
    # When a row ends, the rest of the current byte is skipped
    # A 10x4 image might have data like this:
    #   11111111 11000000
    #   00110100 01000000
    #   00111110 00000000
    #   10111101 11000000
    # Notice how the last 6 bits of each row's last byte are empty.
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    x = 0
    y = 0
    for i in hmsb_data:
        for j in range(8):
            bit = i & (1 << j)
            if bit == 0:
                surface.set_at((x, y), (0, 0, 0, 0))
            else:
                surface.set_at((x, y), (255, 255, 255, 255))
            # Check this at the end of instead of the start, otherwise we skip the last bit of each row
            # if the width is a multiple of 8.
            x += 1
            if x == width:
                x = 0
                y += 1
                break
    return surface

def parse_mono_vlsb(vlsb_data: bytearray, width: int, height: int) -> pygame.Surface:
    # Given the data:
    # 11010100 00001010 ...
    # We basically "rotate" it so that we get:
    # 10...
    # 10...
    # 00...
    # 10...
    # 01...
    # 10...
    # 01...
    # 00...
    # And when we hit the rightmost edge, we advance down 8 pixels
    surface = pygame.Surface((width, height))
    x = 0
    y = 0
    for i in vlsb_data:
        for j in range(8):
            bit = i & (1 << j)
            if bit == 0:
                surface.set_at((x, y + j), (0, 0, 0, 0))
            else:
                surface.set_at((x, y + j), (255, 255, 255, 255))
        x += 1
        if x == width:
            y += 8
            x = 0
    return surface

class FrameBuffer:
    def __init__(self, data: bytearray, width: int, height: int, format: int) -> None:
        if format == MONO_HMSB:
            self.surface = parse_mono_hmsb(data, width, height)
        elif format == MONO_VLSB:
            self.surface = parse_mono_vlsb(data, width, height)
        else:
            print_warning(f"Unknown framebuffer format {format}")
            self.surface = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.format = format

    def color_to_pygame(self, color: int) -> tuple:
        if color == 0:
            return (0, 0, 0, 0)
        return (255, 255, 255, 255)

    def fill(self, color: int):
        self.surface.fill(self.color_to_pygame(color))

    def fill_rect(self, x: int, y: int, width: int, height: int, color: int):
        pygame.draw.rect(self.surface, self.color_to_pygame(color), (x, y, width, height))

    def blit(self, fb, x: int, y: int, key=-1):
        self.surface.blit(fb.surface, (x, y))
