import os
import pygame

WIDTH = 600
HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (64, 64, 64)

platform_speed = 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Tower")
clock = pygame.time.Clock()

script_dir = os.path.dirname(os.path.abspath(__file__))
