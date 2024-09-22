import pygame
import random

# need start screen, win screen, game over/ lose screen, player selector
# fix rock objects to not random spawn
# change images to custom-made ones
# make video presentation for submission
#integrate animations

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat Side Scroller")

#backgound
background = pygame.image.load('background test.png')

# Set up variables for background position
bg_x1 = 0
bg_x2 = WIDTH
bg_speed = 5

# Game variables
cat_speed = 5
fish_collected = 0
cat_health = 3
level_over = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load assets
cat_img = pygame.image.load('cat test.png')  # Add your own cat image here
fish_img = pygame.image.load('fish test.png')  # Add your own fish image here
obstacle_img = pygame.image.load('rock obstacle test.png')  # Add your obstacle image here

# Define game states
START = "start"
PLAYING = "playing"
GAME_OVER = "game_over"
WIN = "win"
game_state = START

# Cat class
class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cat_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT // 2
        self.speed_y = 0

    def update(self):
        # Cat movement
        self.speed_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed_y = -cat_speed
        if keys[pygame.K_DOWN]:
            self.speed_y = cat_speed

        self.rect.y += self.speed_y

        # Keep cat on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = fish_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH + 20, WIDTH + 100)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed_x = random.randint(-8, -4)

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.kill()

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH + 20, WIDTH + 100)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed_x = random.randint(-6, -3)

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.kill()

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
fish_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# Create cat
cat = Cat()
all_sprites.add(cat)

# Clock
clock = pygame.time.Clock()

# Function for showing start screen
def show_start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


# Function for game over screen
def show_game_over_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over! Press R to Restart", True, BLACK)
    screen.blit(text, (WIDTH // 6, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False


# Function for win screen
def show_win_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("You Win! Press R to Restart", True, BLACK)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

# Main game loop
running = True
while running:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == START:
        show_start_screen()
        game_state = PLAYING
        cat_health = 3
        fish_collected = 0
        all_sprites.add(cat)  # Re-add the cat

    elif game_state == PLAYING:
        # Move the background
        bg_x1 -= bg_speed
        bg_x2 -= bg_speed

        if bg_x1 <= -WIDTH:
            bg_x1 = WIDTH
        if bg_x2 <= -WIDTH:
            bg_x2 = WIDTH

        screen.blit(background, (bg_x1, 0))
        screen.blit(background, (bg_x2, 0))

        # Spawn fish and obstacles
        if random.randint(1, 100) < 5:
            fish = Fish()
            all_sprites.add(fish)
            fish_group.add(fish)

        if random.randint(1, 100) < 3:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacle_group.add(obstacle)

        # Update sprites
        all_sprites.update()

        # Check for collisions
        fish_collisions = pygame.sprite.spritecollide(cat, fish_group, True)
        for fish in fish_collisions:
            fish_collected += 1
            if fish_collected >= 5:
                game_state = WIN

        obstacle_collisions = pygame.sprite.spritecollide(cat, obstacle_group, True)
        for obstacle in obstacle_collisions:
            cat_health -= 1
            if cat_health <= 0:
                game_state = GAME_OVER

        # Draw
        all_sprites.draw(screen)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Fish: {fish_collected}  Health: {cat_health}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()

    elif game_state == GAME_OVER:
        show_game_over_screen()
        game_state = START  # Restart the game

    elif game_state == WIN:
        show_win_screen()
        game_state = START  # Restart the game

pygame.quit()