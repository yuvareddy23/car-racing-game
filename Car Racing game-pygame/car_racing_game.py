import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

try:
    background_img = pygame.image.load('road1.png').convert()
    player_img = pygame.image.load('car.png').convert_alpha()
    obstacle_img = pygame.image.load('car1.png').convert_alpha()
except:
    print("Make sure 'road1.png', 'car.png', and 'car1.png' are in the same folder.")
    pygame.quit()
    sys.exit()

background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
player_img = pygame.transform.scale(player_img, (50, 50))
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))

lanes = [75, 175, 275]

player_rect = player_img.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT - 80)

obstacles = []
SPAWN_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACLE, 1500)
speed = 4

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 50)

game_over = False
game_started = False
score = 0
start_time = 0

bg_y1 = 0
bg_y2 = -HEIGHT

def show_start_screen():
    screen.blit(background_img, (0, 0))
    title = big_font.render("Car Racing Game", True, WHITE)
    prompt = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
    pygame.display.flip()

def show_game_over():
    over = big_font.render("Game Over!", True, (255, 0, 0))
    prompt = font.render("Press R to Try Again", True, WHITE)
    screen.blit(over, over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
    screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

def draw_score(seconds):
    score_text = font.render(f"Score: {seconds:.1f}", True, WHITE)
    screen.blit(score_text, (10, 10))

running = True
while running:
    if not game_started:
        show_start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True
                game_over = False
                obstacles.clear()
                player_rect.center = (WIDTH // 2, HEIGHT - 80)
                start_time = pygame.time.get_ticks()
                score = 0
                bg_y1 = 0
                bg_y2 = -HEIGHT

        continue

    screen.blit(background_img, (0, bg_y1))
    screen.blit(background_img, (0, bg_y2))
    bg_y1 += speed
    bg_y2 += speed
    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

    if not game_over:

        for obs in obstacles[:]:
            obs.y += speed
            screen.blit(obstacle_img, obs)
            if obs.colliderect(player_rect):
                game_over = True
            if obs.top > HEIGHT:
                obstacles.remove(obs)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += 5

        screen.blit(player_img, player_rect)

        current_time = pygame.time.get_ticks()
        score = (current_time - start_time) / 1000
        draw_score(score)

    else:
        show_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_OBSTACLE and not game_over:
            lane = random.choice(lanes)
            new_obs = obstacle_img.get_rect(midtop=(lane + 25, -100))
            obstacles.append(new_obs)

    keys = pygame.key.get_pressed()
    if game_over and keys[pygame.K_r]:
        game_over = False
        obstacles.clear()
        player_rect.center = (WIDTH // 2, HEIGHT - 80)
        start_time = pygame.time.get_ticks()
        score = 0
        bg_y1 = 0
        bg_y2 = -HEIGHT

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
