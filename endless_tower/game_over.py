import pygame,os,sys

# Colores
GRAY = (128, 128, 128)
RED = (255, 0, 0)

def show_game_over_screen(screen_width, screen_height):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Over")
    clock = pygame.time.Clock()

    # Configuración de la fuente y el tamaño del texto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "data", "PublicPixel-z84yD.ttf")
    font_name = font_path
    font_size = 48
    font = pygame.font.Font(font_name, font_size)

    show_continue_text = True  # Variable para controlar la visualización del texto "Presione una tecla para continuar"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                running = False  # Salir del bucle cuando se presione una tecla

        screen.fill((0, 0, 0))  # Limpia la pantalla

        text_surface = font.render("YOU DIED", True, RED)
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_width / 2, screen_height / 2)
        screen.blit(text_surface, text_rect)

        if show_continue_text:
            continue_font_size = 12
            continue_font = pygame.font.Font(font_name, continue_font_size)
            continue_text_surface = continue_font.render("Presione una tecla para continuar", True, GRAY)
            continue_text_rect = continue_text_surface.get_rect()
            continue_text_rect.center = (screen_width / 2, screen_height * 3 / 4)
            screen.blit(continue_text_surface, continue_text_rect)

        show_continue_text = not show_continue_text  # Alternar el estado de visualización

        pygame.display.flip()
        clock.tick(1.5)  # Reducir la velocidad de parpadeo ajustando el valor del tick
