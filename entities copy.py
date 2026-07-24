import os
import random
import pygame
from assets import meteor_image, platform_image
from settings import HEIGHT, WIDTH, platform_speed, script_dir

class Player(pygame.sprite.Sprite):
    def __init__(self, platforms, screen):
        super().__init__()
        self.platforms = platforms
        self.screen = screen
        self.animation_list = {"idle": [], "run": [], "jump": [], "die": []}
        self.current_animation = "idle"
        self.animation_index = 0
        self.load_animations()
        self.image = self.animation_list[self.current_animation][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speed_x = 0
        self.speed_y = 0
        self.jump_power = -15
        self.gravity = 0.8
        self.jump_count = 0
        self.max_jump_count = 2
        self.can_move = False
        self.update_time = pygame.time.get_ticks()
        self.is_inverted = False

    def load_animations(self):
        animation_folders = {
            "idle": self.animation_list["idle"],
            "run": self.animation_list["run"],
            "jump": self.animation_list["jump"],
            "die": self.animation_list["die"],
        }
        files_path = os.path.join(script_dir, "data", "player_animations")
        scale_factor = 2
        for animation_name, image_list in animation_folders.items():
            animation_folder_path = os.path.join(files_path, animation_name)
            if not os.path.isdir(animation_folder_path):
                continue
            files = sorted(os.listdir(animation_folder_path))
            for file_name in files:
                if file_name.endswith(".png"):
                    image_path = os.path.join(animation_folder_path, file_name)
                    image = pygame.image.load(image_path).convert_alpha()
                    scaled_image = pygame.transform.scale(
                        image,
                        (image.get_rect().width * scale_factor, image.get_rect().height * scale_factor),
                    )
                    image_list.append(scaled_image)
            if animation_name == "run":
                inverted_images = [pygame.transform.flip(image, True, False) for image in self.animation_list["run"]]
                self.animation_list["run_inverted"] = inverted_images[::-1]

    def update(self):
        if self.can_move:
            self.speed_x = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.speed_x = -5
                self.is_inverted = True
                self.current_animation = "run_inverted"
            elif keys[pygame.K_RIGHT]:
                self.speed_x = 5
                self.is_inverted = False
                self.current_animation = "run"
            else:
                self.current_animation = "idle"
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
            self.speed_y += self.gravity
            self.handle_platform_collision()
            self.play_animation()

    def jump(self):
        if self.jump_count < self.max_jump_count:
            started = False
            if not self.can_move:
                self.can_move = True
                started = True
                for plat in self.platforms:
                    plat.can_move = True
            self.speed_y = self.jump_power
            if self.speed_x != 0:
                self.speed_y -= abs(self.speed_x) * 0.5
            self.jump_count += 1
            self.current_animation = "jump"
            return started
        return False

    def handle_platform_collision(self):
        self.rect.y += 5
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 5
        if hits:
            lowest_platform = max(hits, key=lambda plat: plat.rect.bottom)
            if self.rect.bottom <= lowest_platform.rect.bottom + 10 and self.speed_y >= 0:
                self.rect.bottom = lowest_platform.rect.top
                self.speed_y = 0
                self.jump_count = 0

    def play_animation(self):
        animation_images = self.animation_list[self.current_animation]
        animation_cooldown = 200
        current_time = pygame.time.get_ticks()
        if current_time - self.update_time > animation_cooldown:
            self.update_time = current_time
            self.animation_index += 1
            if self.animation_index >= len(animation_images):
                self.animation_index = 0 if self.current_animation == "jump" else 1
        self.image = animation_images[self.animation_index % len(animation_images)]

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, screen, platforms=None):
        super().__init__()
        self.image = pygame.transform.scale(platform_image, (width, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.can_move = False
        self.screen = screen
        self.platforms = platforms

    def update(self):
        if self.can_move:
            self.rect.y += platform_speed
            if self.rect.top > HEIGHT:
                self.reset_position()

    def reset_position(self):
        self.rect.y = -20
        self.rect.x = self.get_random_x()

    def get_random_x(self):
        valid_x_positions = [x for x in range(0, WIDTH - self.rect.width + 1) if not self.check_collision(x)]
        return random.choice(valid_x_positions) if valid_x_positions else 0

    def check_collision(self, x):
        if self.platforms is None:
            return False
        for plat in self.platforms:
            if plat != self and plat.rect.colliderect(pygame.Rect(x, self.rect.y, self.rect.width, self.rect.height)):
                return True
        return False

class Meteor(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.transform.scale(meteor_image, (40, 50))
        self.rect = self.image.get_rect()
        self.screen = screen
        self.reset_position()

    def update(self):
        self.rect.y += self.fall_speed
        if self.rect.y > HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.y = random.randint(-HEIGHT, 0)
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.fall_speed = random.randint(3, 5)
