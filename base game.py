import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2D Side-Scrolling Game')

# Clock object to control frame rate
clock = pygame.time.Clock()

# Load background image (replace 'background.png' with your image file)
background = pygame.image.load('desert_background.png')
background_width = background.get_width()

# Load character image (replace 'character.png' with your image file)
character = pygame.image.load('character.png')
character = pygame.transform.scale(character, (50, 50))  # Resize character

# Variables for background scrolling
scroll_speed = 5
background_x = 0

# Player character position
player_x = 50
player_y = 300
player_speed_y = 0
jumping = False
GRAVITY = 0.5
JUMP_STRENGTH = 10

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                player_speed_y = -JUMP_STRENGTH
                jumping = True

    # Apply gravity
    player_speed_y += GRAVITY
    player_y += player_speed_y

    # Stop the character from falling off the screen
    if player_y >= 300:
        player_y = 300
        jumping = False

    # Scroll background
    background_x -= scroll_speed
    if background_x <= -background_width:
        background_x = 0

    # Fill screen with white
    screen.fill(WHITE)

    # Draw the background twice to create the scrolling effect
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + background_width, 0))

    # Draw the player character
    screen.blit(character, (player_x, player_y))

    # Update the display
    pygame.display.update()

    # Frame rate
    clock.tick(60)

pygame.quit()

#pleaseeee