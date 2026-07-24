import os
import pygame

class SoundManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sound_dir = os.path.join(base_dir, "data", "sounds")
        self.jump_sound = pygame.mixer.Sound(os.path.join(sound_dir, "jump.mp3"))
        pygame.mixer.music.load(os.path.join(sound_dir, "theme.mp3"))
        self.background_music_started = False

    def play_jump_sound(self):
        self.jump_sound.set_volume(0.1)
        self.jump_sound.play()

    def play_background_music(self):
        if not self.background_music_started:
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            self.background_music_started = True
