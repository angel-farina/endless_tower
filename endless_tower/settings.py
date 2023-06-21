import pygame,os

# Configuración de la ventana
WIDTH = 600
HEIGHT = 800
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (64, 64, 64)

# Variables globales
name = ""
score = 0
platform_speed = 2

# Inicialización de Pygame y creación de la ventana
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Tower")
clock = pygame.time.Clock()

# Imagenes rutas y carga
# Obtener la ruta del directorio actual del script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Cargar la imagen del jugador
player_image_path = os.path.join(script_dir, "data", "player1.png")
player_image = pygame.image.load(player_image_path).convert_alpha()
# Cargar la imagen de las plataformas
platform_image_path = os.path.join(script_dir, "data", "platform.png")
platform_image = pygame.image.load(platform_image_path).convert_alpha()
# Cargar la imagen del fondo
platform_image_path = os.path.join(script_dir, "data", "space3.jpg")
background_image = pygame.image.load(platform_image_path).convert()
# Cargar la imagen del agujero negro
#blackhole_image_path = os.path.join(script_dir, "data", "blackhole.png")
#blackhole_image = pygame.image.load(blackhole_image_path).convert_alpha()
# Cargar la imagen de los meteoros
meteor_image_path = os.path.join(script_dir, "data", "meteor.png")
meteor_image = pygame.image.load(meteor_image_path).convert_alpha()