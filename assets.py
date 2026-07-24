import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "data")

platform_image_path = os.path.join(ASSET_DIR, "background", "platform.png")
background_image_path = os.path.join(ASSET_DIR, "background", "space3.jpg")
meteor_image_path = os.path.join(ASSET_DIR, "effects", "meteor.png")

platform_image = pygame.image.load(platform_image_path)
background_image = pygame.image.load(background_image_path)
meteor_image = pygame.image.load(meteor_image_path)
