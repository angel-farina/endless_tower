import os
import pygame

GRAY = (128, 128, 128)
RED = (255, 0, 0)

def show_game_over_screen(screen, screen_width, screen_height):
    clock = pygame.time.Clock()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, "data", "fonts", "PublicPixel-z84yD.ttf")
    font = pygame.font.Font(font_path, 48)

    show_continue_text = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                return "restart"

        screen.fill((0, 0, 0))
        text_surface = font.render("YOU DIED", True, RED)
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_width / 2, screen_height / 2)
        screen.blit(text_surface, text_rect)

        if show_continue_text:
            continue_font = pygame.font.Font(font_path, 12)
            continue_text_surface = continue_font.render("Presione una tecla para continuar", True, GRAY)
            continue_text_rect = continue_text_surface.get_rect()
            continue_text_rect.center = (screen_width / 2, screen_height * 3 / 4)
            screen.blit(continue_text_surface, continue_text_rect)

        show_continue_text = not show_continue_text
        pygame.display.flip()
        clock.tick(1.5)
