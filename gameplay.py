#####################################
# IMPORTS
#####################################
import pygame
import random
import sys

#####################################
# FRAME, COLOR & FONT
#####################################

# FRAME
width = 640
height = 400
FPS = 30


# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# FONT
font_name = pygame.font.match_font('arial')

####################################
# INITIALIZATIONS
####################################

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()  # for sound effects and music (currently not included)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy")
clock = pygame.time.Clock()


# Load all game graphics (ENSURE FILE PATHS ARE CORRECT)
background = pygame.image.load('field.png').convert()
background_rect = background.get_rect()
flappy_1 = pygame.image.load('flappy/frame-1.png').convert()
flappy_2 = pygame.image.load('flappy/frame-2.png').convert()
flappy_3 = pygame.image.load('flappy/frame-3.png').convert()
ublock = pygame.image.load('ublock.png').convert()
lblock = pygame.image.load('lblock.png').convert()


# Load all game sounds (CURRENTLY NOT IN USE)
# jump_sound = pygame.mixer.Sound('name_of_file.wav')
# pygame.mixer.music.load('name_of_file.mp3')
# pygame.mixer.music.set_volume(0.4)
# pygame.mixer.music.play()


#####################################
# FUNCTIONS
#####################################

# FUNCTION FOR UPPER AND LOWER BLOCKS TO CONTINUOUSLY APPEAR
def block_loop():
    # Initialing each new block (Note: block .png files are 299 pixels in height)
    # NOTE: First blocks (upper and lower) that appear are initialized in the Game Loop
    upper_block_h = random.randrange(-299, 0)
    lower_block_h = upper_block_h + 100 + 299  # 100 pixel space range between blocks

    new_upper_block, new_lower_block = UpperBlock(upper_block_h), LowerBlock(lower_block_h)

    blocks.add(new_upper_block, new_lower_block)
    all_sprites.add(new_upper_block, new_lower_block)


# FUNCTION TO DISPLAY TEXT
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


# HOME SCREEN
def home_screen():

    # Keeping track of high score using a .txt file
    with open('highscore.txt', 'r') as x:
        high_score = int(x.read())

    # Home Screen
    screen.blit(background, background_rect)
    draw_text(screen, "FLAPPY", 72, width/2, height/3)
    draw_text(screen, "Press 'space bar' to jump higher", 22, width/2, height/1.8)
    draw_text(screen, "Press 'f' to begin", 22, width/2, height/1.5)
    draw_text(screen, "High Score: {}".format(str(high_score)), 16, 580, 20)
    pygame.display.flip()

    # Waiting for game to be initialized (pressing 'f' to begin)
    waiting = True
    while waiting:
        # pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    waiting = False


#####################################
# CLASSES/SPRITES
#####################################

# PLAYER (BIRD) SPRITE
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []  # 3 flappy images (for flapping wings)
        self.images.append(flappy_1)
        self.images.append(flappy_2)
        self.images.append(flappy_3)
        self.index = 0
        self.image = pygame.transform.scale(self.images[self.index], (50, 40))
        self.image.set_colorkey(white)
        self.rect = pygame.rect.Rect((0, 0), (45, 36))
        # print(self.rect)
        self.radius = 18
        self.rect.center = (width / 5, height / 2)
        self.y_speed = 0

    def update(self):
        global game_over
        self.y_speed = 3  # constantly moving down
        self.rect.y += self.y_speed
        self.index += 1  # for flapping wings

        if self.index >= len(self.images):
            self.index = 0  # start at first image after going through all the flap images

        self.image = pygame.transform.scale(self.images[self.index], (50, 40))
        self.image.set_colorkey(white)

        # If player presses the space bar, move up
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.rect.y += -13
        self.rect.y += self.y_speed

        # Player cannot go above the top of the frame
        if self.rect.top < 0:
            self.rect.y = 0

        # If player is too low, game over!
        if self.rect.top > height:
            game_over = True


# UPPER BLOCK SPRITES
class UpperBlock(pygame.sprite.Sprite):

    def __init__(self, upper_block_h):
        pygame.sprite.Sprite.__init__(self)
        self.image = ublock
        # self.image.set_colorkey(white)  # Not needed since no white around sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (width, upper_block_h)
        self.x_speed = 0

    def update(self):
        global score
        self.x_speed = -4.5
        self.rect.x += self.x_speed

        if self.rect.right == 440:
            block_loop()  # after first blocks appear, call block_loop() for continuous blocks to appear

        # For Keeping Scores (including Hi-Score)
        if self.rect.right == 130:  # flappy passes blocks at 130 pixels (x-width)
            score += 1
            with open('highscore.txt', 'r') as x:
                high_score = int(x.read())
            if score > high_score:
                with open('highscore.txt', 'w') as textfile:
                    print(score, file=textfile)

        if self.rect.right < 0:  # remove once off-screen
            self.kill()


# LOWER BLOCK SPRITES
class LowerBlock(pygame.sprite.Sprite):

    def __init__(self, lower_block_h):
        pygame.sprite.Sprite.__init__(self)
        self.image = lblock
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.topleft = (width, lower_block_h)
        self.x_speed = 0

    def update(self):
        self.x_speed = -4.5
        self.rect.x += self.x_speed

        if self.rect.right < 0:  # remove once off-screen
            self.kill()


#####################################
# GAME LOOP
#####################################

game_over = True  # Start at home Screen
running = True

while running:
    if game_over:
        score = 0
        home_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()

        # Start a new game:
        blocks = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        init_upper_block_h = random.randrange(-299, 0)
        init_lower_block_h = init_upper_block_h + 100 + 299
        first_blockU = UpperBlock(init_upper_block_h)
        first_blockL = LowerBlock(init_lower_block_h)

        blocks.add(first_blockU)
        blocks.add(first_blockL)
        all_sprites.add(first_blockU)
        all_sprites.add(first_blockL)

    # Keep loop running at the right speed
    clock.tick(FPS)

    # Process Input (Events)
    for event in pygame.event.get():
        # check for closing window while game is running
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    # Update
    all_sprites.update()

    # Check to see if player gets hit
    hits = pygame.sprite.spritecollide(player, blocks, False)
    # False controls whether or not the sprite you hit is deleted or not

    # Draw / Render
    screen.fill(white)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 36, width/2, 30)
    if hits:
        game_over = True

    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
