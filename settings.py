import pygame
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 640, 360
TILE_SIZE = 32
WINDOW_CAPTION = "feibg's Game"
FPS = 60