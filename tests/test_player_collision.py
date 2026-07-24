import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

try:
    import pygame
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from entities import Platform, Player
except ModuleNotFoundError:  # pragma: no cover
    pygame = None
    Platform = Player = None

@unittest.skipIf(pygame is None, "pygame is not available in this environment")
class PlayerCollisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_player_lands_on_platform(self):
        screen = pygame.display.set_mode((600, 800))
        platforms = pygame.sprite.Group()
        platform = Platform(100, 500, 120, screen, platforms)
        platforms.add(platform)
        player = Player(platforms, screen)
        player.can_move = True
        player.rect.x = 120
        player.rect.bottom = 490
        player.speed_y = 5

        player.handle_platform_collision()

        self.assertEqual(player.rect.bottom, platform.rect.top)
        self.assertEqual(player.speed_y, 0)
        self.assertEqual(player.jump_count, 0)

if __name__ == "__main__":
    unittest.main()
