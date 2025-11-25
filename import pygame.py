import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
window_x = 720
window_y = 480
game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Pygame Snake')

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Snake properties
snake_speed = 15
snake_block_size = 10
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction

# Food properties
food_position = [random.randrange(1, (window_x // snake_block_size)) * snake_block_size,
                 random.randrange(1, (window_y // snake_block_size)) * snake_block_size]
food_spawn = True

# Score
score = 0

# Game Over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Game Over!', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    quit()

# Show Score function
def show_score(choice=1):
    score_font = pygame.font.SysFont('times new roman', 20)
    score_surface = score_font.render('Score : ' + str(score), True, white)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (80, 10)
    else:
        score_rect.midtop = (window_x / 2, window_y / 1.5)
    game_window.blit(score_surface, score_rect)

# Game Loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Validate direction change
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_position[1] -= snake_block_size
    if direction == 'DOWN':
        snake_position[1] += snake_block_size
    if direction == 'LEFT':
        snake_position[0] -= snake_block_size
    if direction == 'RIGHT':
        snake_position[0] += snake_block_size

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 10
        food_spawn = False
    else:
        snake_body.pop()

    # Spawn food
    if not food_spawn:
        food_position = [random.randrange(1, (window_x // snake_block_size)) * snake_block_size,
                         random.randrange(1, (window_y // snake_block_size)) * snake_block_size]
    food_spawn = True

    # Drawing
    game_window.fill(black)
    for block in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(block[0], block[1], snake_block_size, snake_block_size))
    pygame.draw.rect(game_window, white, pygame.Rect(food_position[0], food_position[1], snake_block_size, snake_block_size))

    # Game Over conditions
    # Wall collision
    if snake_position[0] < 0 or snake_position[0] > window_x - snake_block_size or \
       snake_position[1] < 0 or snake_position[1] > window_y - snake_block_size:
        game_over()

    # Self-collision
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Update display
    show_score()
    pygame.display.update()

    # Control game speed
    clock.tick(snake_speed)

pygame.quit()