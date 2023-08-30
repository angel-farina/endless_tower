import pygame,os,pygame.mixer

# Clase para el manejo de sonidos
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.jump_sound = pygame.mixer.Sound(os.path.join(script_dir, "data/sounds", "jump.mp3"))
        self.background_music = pygame.mixer.music.load(os.path.join(script_dir, "data/sounds", "theme.mp3"))
        
    def play_jump_sound(self):
        self.jump_sound.set_volume(0.1)
        self.jump_sound.play()
    
    def play_background_music(self):
        pygame.mixer.music.set_volume(0.1)  # Volumen música (0.2 = 20% del volumen máximo)
        pygame.mixer.music.play(-1)  # Reproducir en bucle (-1 indica bucle infinito)
