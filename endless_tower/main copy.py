import pygame,random,os,database
from game_over import show_game_over_screen
from database import create_scores_table,save_score, check_if_table_exists,get_highest_score, get_highscore_name
from sound import SoundManager

# Configuración de la ventana
WIDTH = 600
HEIGHT = 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (64, 64, 64)

# Variables globales
name = ""
score = 0

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

# Clase para el personaje principal
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((50, 50))
        #self.image.fill(BLUE)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT  # Posición inicial en la parte inferior de la pantalla
        self.speed_x = 0
        self.speed_y = 0
        self.jump_power = -15
        self.gravity = 0.8
        self.jump_count = 0
        self.max_jump_count = 2
        self.can_move = False

    def update(self):
        if self.can_move:
            self.speed_x = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.speed_x = -5
            if keys[pygame.K_RIGHT]:
                self.speed_x = 5

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

            self.speed_y += self.gravity
            self.handle_platform_collision()

    def jump(self):
        global game_started
        if self.jump_count < self.max_jump_count:
            if not self.can_move:
                self.can_move = True  # Habilitar el movimiento al primer salto
                for plat in platforms:
                    plat.can_move = True
                game_started = True  # Iniciar el juego y detener la visualización del texto inicial
            self.speed_y = self.jump_power
            if self.speed_x != 0:
                self.speed_y -= abs(self.speed_x) * 1.5
            self.jump_count += 1

    def handle_platform_collision(self):
        self.rect.y += 5  # Actualizar posición del jugador antes de verificar las colisiones
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 5  # Restaurar posición del jugador

        if hits:
            lowest_platform = max(hits, key=lambda plat: plat.rect.bottom)
            if self.rect.bottom <= lowest_platform.rect.bottom + 10 and self.speed_y >= 0:
                self.rect.bottom = lowest_platform.rect.top
                self.speed_y = 0
                self.jump_count = 0

# Clase para las plataformas
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((width, 20))
        #self.image.fill(WHITE)
        self.image = platform_image
        self.image = pygame.transform.scale(self.image, (width, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.can_move = False

    def update(self):
        if self.can_move:
            self.rect.y += 2
            if self.rect.top > HEIGHT:
                self.reset_position()

    def reset_position(self):
        self.rect.y = -20  # Colocar la plataforma arriba de la pantalla
        self.rect.x = self.get_random_x()

    def get_random_x(self):
        valid_x_positions = [x for x in range(0, WIDTH - self.rect.width + 1) if not self.check_collision(x)]
        return random.choice(valid_x_positions)

    def check_collision(self, x):
        for plat in platforms:
            if plat != self and plat.rect.colliderect(pygame.Rect(x, self.rect.y, self.rect.width, self.rect.height)):
                return True
        return False

# Clase meteoro
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = meteor_image
        self.image = pygame.transform.scale(self.image, (40, 50))  # Tamaño de los meteoros
        self.rect = self.image.get_rect()
        self.reset_position()
    
    def update(self):
        self.rect.y += self.fall_speed
        if self.rect.y > HEIGHT:
            self.reset_position()
    
    def reset_position(self):
        self.rect.y = random.randint(-HEIGHT, 0)
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Posición horizontal aleatoria
        self.fall_speed = random.randint(3, 5)  # Velocidad de caída aleatoria

# Parallax inicializaciones
# Velocidades de desplazamiento para cada capa del fondo
parallax_speeds = [1, 0.5, 0.2]
# Posiciones iniciales de cada capa del fondo
parallax_offsets = [0, 0, 0]

# Creación de grupos de sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
meteors = pygame.sprite.Group()

# Creación del personaje principal
player = Player()
all_sprites.add(player)

# Creación de los meteoros
for i in range(1):
    meteor = Meteor()
    meteor.rect.x = random.randrange(0, WIDTH)
    meteor.rect.y = random.randrange(-HEIGHT, 0)
    meteors.add(meteor)
    all_sprites.add(meteor)

# Creación de las plataformas
platform_y = HEIGHT - 100  # Altura inicial de las plataformas
for i in range(10):
    plat_width = random.randint(50, 200)  # Ancho aleatorio de las plataformas

    plat = Platform(random.randint(0, WIDTH - plat_width), platform_y, plat_width)
    platforms.add(plat)
    all_sprites.add(plat)

    platform_y -= random.randint(100, 200)  # Espacio aleatorio entre plataformas

def initial_text():
    # Configuración de la fuente y el tamaño del texto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "data", "PublicPixel-z84yD.ttf")
    font_name = font_path
    font_size = 11
    font = pygame.font.Font(font_name, font_size)

    # Renderizar texto en una superficie
    text_surface = font.render("Presiona cualquier tecla para comenzar", True, WHITE)

    # Centrar el texto en la pantalla
    text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    # Dibujar el texto en la pantalla
    screen.blit(text_surface, text_rect)

def show_score(score):
    # Configuración de la fuente y el tamaño del texto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "data", "PublicPixel-z84yD.ttf")
    font_name = font_path
    font_size = 15
    font = pygame.font.Font(font_name, font_size)

    # Renderizar el texto del puntaje
    score_text = font.render("Score: " + str(int(score)), True, WHITE)
    screen.blit(score_text, (10, 10))  # Dibuja el texto del puntaje en la posición (10, 10)

    # Obtener el puntaje más alto y el nombre asociado
    highest_score = database.get_highest_score()
    highest_score_text = font.render("High Score: " + str(highest_score), True, WHITE)
    screen.blit(highest_score_text, (350, 10))  # Dibuja el texto del puntaje más alto en la posición (10, 30)

    #speed_text = font.render("Level: " + str(), True, DARK_GRAY)
    #screen.blit(speed_text, (10, 30))  # Dibuja el texto de la velocidad en la posición (10, 30)

    if highest_score > 0:
        highest_score_name = database.get_highscore_name()
        name_text = font.render("Name: " + highest_score_name, True, WHITE)
        screen.blit(name_text, (350, 30))  # Dibuja el texto del nombre asociado al puntaje más alto en la posición (10, 50)

def get_name():
    global name
    input_box = pygame.Rect(150, 400, 300, 40)
    name = ""
    is_typing = True

    while is_typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_typing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill(BLACK)

        # Configuración de la fuente y el tamaño del texto
        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, "data", "PublicPixel-z84yD.ttf")
        font_name = font_path
        font_size = 30
        font_size_dos = 12
        font = pygame.font.Font(font_name, font_size)
        font_dos = pygame.font.Font(font_name, font_size_dos)

        # Obtener el ancho y alto del texto
        text_width, text_height = font.size("New Record!")

        # Calcular las coordenadas para centrar el texto y la entrada de texto
        text_x = (WIDTH - text_width) // 2
        text_y = (HEIGHT - text_height) // 2 - 50

        input_box_x = (WIDTH - input_box.width) // 2
        input_box_y = (HEIGHT - input_box.height) // 2 + 50

        text = font.render("NEW RECORD!", True, WHITE)
        screen.blit(text, (text_x, text_y))

        text_surface = font_dos.render(name, True, WHITE)
        text_width = text_surface.get_width()  # Obtener el ancho del texto ingresado
        screen.blit(text_surface, (input_box_x + (input_box.width - text_width) // 2, input_box_y))  # Centrar el texto ingresado

        # Agregar una nueva línea de texto debajo de "NEW RECORD!"
        new_line_text = font_dos.render("↓ Ingresa tu nombre ↓", True, DARK_GRAY)
        new_line_text_x = (WIDTH - new_line_text.get_width()) // 2
        new_line_text_y = text_y + text_height + 20
        screen.blit(new_line_text, (new_line_text_x, new_line_text_y))

        pygame.display.flip()
        clock.tick(30)

# Crear la db
create_scores_table()

# Variable para controlar si el juego ha comenzado
game_started = False

# Obtener el puntaje guardado en la base de datos
highest_score = 0  # Puntaje más alto inicial
if check_if_table_exists():
    highest_score = get_highest_score()

# Crear una instancia del SoundManager
sound_manager = SoundManager()

# Reproducir la música de fondo constantemente
sound_manager.play_background_music()

# Ciclo del juego
running = True
while running:
    clock.tick(FPS)

    # Eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
                sound_manager.play_jump_sound()

    # Actualización
    all_sprites.update()
    # Actualizar los meteoros
    meteors.update()

    # Verificar si el jugador pierde
    hits = pygame.sprite.spritecollide(player, meteors, False)
    if player.rect.top > HEIGHT or hits:
        if score > highest_score:
            get_name()
            
        show_game_over_screen(WIDTH, HEIGHT)
        # Conectar a la base de datos y guardar el nombre y el puntaje
        save_score(name, score)
        running = False  # Salir del bucle principal después de mostrar la pantalla de Game Over

    # Dibujado en pantalla
    screen.fill((0, 0, 0))  # Limpia la pantalla

    # Control Parallax
    for i in range(len(parallax_speeds)):
        # Calcula el desplazamiento de la capa en función de la velocidad
        parallax_offsets[i] += parallax_speeds[i]

        # Si la capa se ha desplazado más allá de la pantalla, reinicia su posición
        if parallax_offsets[i] >= HEIGHT:
            parallax_offsets[i] = 0

        # Dibuja la capa en la pantalla teniendo en cuenta el desplazamiento
        screen.blit(background_image, (0, parallax_offsets[i] - HEIGHT))

    if not game_started:  # Verificar si el juego ha comenzado
        initial_text()
    else:
        #screen.blit(background_image, (0, 0))  # Dibuja la imagen de fondo en la posición (0, 0)
        all_sprites.draw(screen)
        screen.blit(player.image, player.rect)  # Dibuja la imagen del jugador

        # Incrementar el puntaje en función del tiempo transcurrido
        score += clock.get_time() / 1000  # Divide el tiempo en milisegundos por 1000 para obtener segundos

        # Mostrar el puntaje en pantalla
        show_score(score)

    # Actualización de la pantalla
    pygame.display.flip()

pygame.quit()
