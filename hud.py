import os
import pygame
import database
from settings import HEIGHT, WHITE, WIDTH, script_dir

class HUD:
    def __init__(self):
        self.font_path = os.path.join(script_dir, "data", "fonts", "PublicPixel-z84yD.ttf")

    def draw_initial_text(self, screen):
        font = pygame.font.Font(self.font_path, 11)
        
        # Mensaje principal
        text_surface = font.render(
            "Presiona cualquier tecla para comenzar",
            True,
            WHITE
        )
        text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 40))
        screen.blit(text_surface, text_rect)

        # Titulo del ranking
        ranking = database.get_top_scores(5)

        ranking_title = font.render("HIGH SCORES", True, WHITE)
        ranking_rect = ranking_title.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 20))
        screen.blit(ranking_title, ranking_rect)

        # Columnas
        x_pos = WIDTH / 2 - 95      # 1.
        x_name = WIDTH / 2 - 65     # Nombre
        x_score = WIDTH / 2 + 90    # Puntaje (columna fija)

        # Ranking
        for i, (name, score) in enumerate(ranking):
            y = HEIGHT / 2 + 50 + i * 15

            pos_surface = font.render(f"{i+1}.", True, WHITE)
            name_surface = font.render(name, True, WHITE)
            score_surface = font.render(str(score), True, WHITE)

            screen.blit(pos_surface, (x_pos, y))
            screen.blit(name_surface, (x_name, y))

            # Alineado a la derecha
            screen.blit(
                score_surface,
                (x_score - score_surface.get_width(), y)
            )

    def draw_score(self, screen, score):
        font = pygame.font.Font(self.font_path, 15)
        score_text = font.render("Score: " + str(int(score)), True, WHITE)
        screen.blit(score_text, (10, 10))
        highest_score = database.get_highest_score()
        highest_score_text = font.render("High Score: " + str(highest_score), True, WHITE)
        screen.blit(highest_score_text, (350, 10))
        if highest_score > 0:
            highest_score_name = database.get_highscore_name()
            name_text = font.render("Name: " + highest_score_name, True, WHITE)
            screen.blit(name_text, (350, 30))
