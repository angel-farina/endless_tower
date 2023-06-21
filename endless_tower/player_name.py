import pygame
from pygame.locals import *


def get_player_name(screen, clock):
    font = pygame.font.Font(None, 32)
    initials = ""
    active = True
    max_initials = 3

    while active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None
            elif event.type == KEYDOWN:
                if event.key == K_RETURN and len(initials) == max_initials:
                    active = False
                elif event.key == K_BACKSPACE:
                    initials = initials[:-1]
                else:
                    key = pygame.key.name(event.key)
                    if key.isalpha() and len(initials) < max_initials:
                        initials += key.upper()

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (200, 250, 400, 100), 2)

        input_text = font.render(initials, True, (0, 0, 0))
        screen.blit(input_text, (350, 270))

        pygame.display.flip()
        clock.tick(30)

    return initials