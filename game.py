import os
import random
import pygame
import database
from assets import background_image
from entities import Meteor, Platform, Player
from game_over import show_game_over_screen
from hud import HUD
from settings import BLACK, DARK_GRAY, FPS, HEIGHT, WHITE, WIDTH, clock, screen, script_dir
from sound import SoundManager

class Game:
    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.name = ""
        self.score = 0
        self.highest_score = 0
        self.game_started = False
        self.parallax_speeds = [1, 0.5, 0.2]
        self.parallax_offsets = [0, 0, 0]
        self.hud = HUD()
        self.sound_manager = SoundManager()
        self.reset_game_state()

    def reset_game_state(self):
        self.name = ""
        self.score = 0
        self.highest_score = database.get_highest_score() if database.check_if_table_exists() else 0
        self.game_started = False
        self.parallax_offsets = [0, 0, 0]
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.player = Player(self.platforms, self.screen)
        self.all_sprites.add(self.player)
        self._create_meteors()
        self._create_platforms()

    def _create_meteors(self):
        for _ in range(1):
            meteor = Meteor(self.screen)
            meteor.rect.x = random.randrange(0, WIDTH)
            meteor.rect.y = random.randrange(-HEIGHT, 0)
            self.meteors.add(meteor)
            self.all_sprites.add(meteor)

    def _create_platforms(self):
        platform_y = HEIGHT - 100
        for _ in range(10):
            plat_width = random.randint(50, 200)
            plat = Platform(random.randint(0, WIDTH - plat_width), platform_y, plat_width, self.screen, self.platforms)
            self.platforms.add(plat)
            self.all_sprites.add(plat)
            platform_y -= random.randint(100, 200)

    def get_name(self):
        input_box = pygame.Rect(150, 400, 300, 40)
        self.name = ""
        is_typing = True
        max_name_length = 12
        font_path = os.path.join(script_dir, "data", "fonts", "PublicPixel-z84yD.ttf")

        while is_typing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_typing = False
                    elif event.key == pygame.K_ESCAPE:
                        self.name = "N/A"
                        is_typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif len(self.name) < max_name_length and event.unicode.isprintable():
                        self.name += event.unicode

            self.screen.fill(BLACK)
            font = pygame.font.Font(font_path, 30)
            font_small = pygame.font.Font(font_path, 12)
            text_width, text_height = font.size("New Record!")
            text_x = (WIDTH - text_width) // 2
            text_y = (HEIGHT - text_height) // 2 - 50
            input_box_x = (WIDTH - input_box.width) // 2
            input_box_y = (HEIGHT - input_box.height) // 2 + 50
            text = font.render("NEW RECORD!", True, WHITE)
            self.screen.blit(text, (text_x, text_y))
            text_surface = font_small.render(self.name, True, WHITE)
            text_width = text_surface.get_width()
            self.screen.blit(text_surface, (input_box_x + (input_box.width - text_width) // 2, input_box_y))
            new_line_text = font_small.render("↓ Ingresa tu nombre ↓", True, DARK_GRAY)
            new_line_text_x = (WIDTH - new_line_text.get_width()) // 2
            new_line_text_y = text_y + text_height + 20
            self.screen.blit(new_line_text, (new_line_text_x, new_line_text_y))
            pygame.display.flip()
            self.clock.tick(30)

    def handle_game_over(self):
        if self.score > self.highest_score:
            self.get_name()
        result = show_game_over_screen(self.screen, WIDTH, HEIGHT)
        database.save_score(self.name, self.score)
        return result

    def update_parallax(self):
        for i in range(len(self.parallax_speeds)):
            self.parallax_offsets[i] += self.parallax_speeds[i]
            if self.parallax_offsets[i] >= HEIGHT:
                self.parallax_offsets[i] = 0
            self.screen.blit(background_image, (0, self.parallax_offsets[i] - HEIGHT))

    def run(self):
        database.create_scores_table()
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    started = self.player.jump()
                    self.game_started = self.game_started or started
                    self.sound_manager.play_jump_sound()

            self.all_sprites.update()
            self.meteors.update()

            if self.game_started:
                hits = pygame.sprite.spritecollide(self.player, self.meteors, False)
                if self.player.rect.top > HEIGHT or hits:
                    result = self.handle_game_over()
                    if result == "restart":
                        self.reset_game_state()
                        continue
                    self.running = False
                    break

            self.screen.fill((0, 0, 0))
            self.update_parallax()
            if not self.game_started:
                self.hud.draw_initial_text(self.screen)
                self.sound_manager.play_background_music()
            else:
                self.all_sprites.draw(self.screen)
                self.score += self.clock.get_time() / 1000
                self.hud.draw_score(self.screen, self.score)

            pygame.display.flip()
