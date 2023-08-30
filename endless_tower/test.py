import pygame
import os

WIDTH = 800
HEIGHT = 600

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Directorio del script actual
script_dir = os.path.dirname(__file__)

# Clase Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = {
            "idle": [],
            "run": [],
            "jump": [],
            "die": []
        }
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
            "die": self.animation_list["die"]
        }

        files_path = os.path.join(script_dir, 'data', 'player_animations')
        scale_factor = 2

        for animation_name, image_list in animation_folders.items():
            animation_folder_path = os.path.join(files_path, animation_name)
            files = sorted(os.listdir(animation_folder_path))

            for file_name in files:
                if file_name.endswith(".png"):
                    image_path = os.path.join(animation_folder_path, file_name)
                    image = pygame.image.load(image_path).convert_alpha()
                    scaled_image = pygame.transform.scale(image, (image.get_rect().width * scale_factor, image.get_rect().height * scale_factor))
                    image_list.append(scaled_image)

            if animation_name == "run":
                inverted_images = []
                for image in self.animation_list["run"]:
                    inverted_image = pygame.transform.flip(image, True, False)
                    inverted_images.append(inverted_image)
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
            screen.blit(self.image, self.rect)

    def jump(self):
        global game_started
        if self.jump_count < self.max_jump_count:
            if not self.can_move:
                self.can_move = True
                for plat in platforms:
                    plat.can_move = True
                game_started = True
            self.speed_y = self.jump_power
            if self.speed_x != 0:
                self.speed_y -= abs(self.speed_x) * 0.5
            self.jump_count += 1
            self.current_animation = "jump"

    def handle_platform_collision(self):
        self.rect.y += 5
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 5

        if hits:
            lowest_platform = max(hits, key=lambda plat: plat.rect.bottom)
            if self.rect.bottom <= lowest_platform.rect.bottom + 10 and self.speed_y >= 0:
                self.rect.bottom = lowest_platform.rect.top
                self.speed_y = 0
                self.jump_count = 0

    def play_animation(self):
        animation_images = self.animation_list[self.current_animation]

        current_time = pygame.time.get_ticks()
        animation_cooldown = 200

        if current_time - self.update_time > animation_cooldown:
            self.update_time = current_time
            self.animation_index = (self.animation_index + 1) % len(animation_images)

        self.image = animation_images[self.animation_index]

# Clase Platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.can_move = False

    def update(self):
        if self.can_move:
            self.rect.x += 1
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.can_move = False

# Inicialización del juego
player = Player()
platforms = pygame.sprite.Group()
platforms.add(Platform(100, HEIGHT - 100))
platforms.add(Platform(400, HEIGHT - 200))
platforms.add(Platform(700, HEIGHT - 300))

game_started = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_started:
                player.jump()

    screen.fill((0, 0, 0))
    platforms.update()
    player.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
