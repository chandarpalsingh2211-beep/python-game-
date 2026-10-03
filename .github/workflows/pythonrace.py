 
import pygame 
import random 
import sys 
 
pygame.init() 
 
# Window settings 
WIDTH, HEIGHT = 500, 700 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Python Car Racing Game") 
 
clock = pygame.time.Clock() 
font = pygame.font.SysFont("Arial", 28, bold=True) 
small_font = pygame.font.SysFont("Arial", 20) 
 
# Colors 
WHITE = (255, 255, 255) 
BLACK = (25, 25, 25) 
GRAY = (65, 65, 65) 
GREEN = (30, 130, 50) 
RED = (240, 40, 50) 
BLUE = (40, 130, 255) 
YELLOW = (255, 220, 0) 
 
# Road settings 
ROAD_LEFT = 70 
ROAD_WIDTH = 360 
LANE_WIDTH = ROAD_WIDTH // 3 
 
CAR_W, CAR_H = 45, 75 
player_x = WIDTH // 2 - CAR_W // 2 
player_y = HEIGHT - 120 
 
enemy_x = random.choice([ 
    ROAD_LEFT + 25, 
    ROAD_LEFT + LANE_WIDTH + 25, 
    ROAD_LEFT + 2 * LANE_WIDTH + 25 
]) 
enemy_y = -100 
 
score = 0 
speed = 5 
game_over = False 
paused = False 
road_line_y = 0 
 
 
def draw_car(x, y, color): 
    # Car body 
    pygame.draw.rect( 
        screen, color, 
        (x, y, CAR_W, CAR_H), 
        border_radius=9 
    ) 
 
    # Windows 
    pygame.draw.rect( 
        screen, (180, 220, 240), 
        (x + 8, y + 10, CAR_W - 16, 18), 
        border_radius=4 
    ) 
    pygame.draw.rect( 
        screen, (30, 35, 45), 
        (x + 8, y + 37, CAR_W - 16, 20), 
        border_radius=3 
    ) 
 
    # Headlights 
    pygame.draw.rect(screen, WHITE, (x + 5, y + 3, 9, 5)) 
    pygame.draw.rect(screen, WHITE, (x + 31, y + 3, 9, 5)) 
 
 
def reset_game(): 
    global player_x, enemy_x, enemy_y 
    global score, speed, game_over, paused, road_line_y 
 
    player_x = WIDTH // 2 - CAR_W // 2 
    enemy_x = random.choice([ 
        ROAD_LEFT + 25, 
        ROAD_LEFT + LANE_WIDTH + 25, 
        ROAD_LEFT + 2 * LANE_WIDTH + 25 
    ]) 
    enemy_y = -100 
    score = 0 
    speed = 5 
    game_over = False 
    paused = False 
    road_line_y = 0 
 
 
running = True 
 
while running: 
    clock.tick(60) 
 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE: 
                running = False 
 
            if event.key == pygame.K_p and not game_over: 
                paused = not paused 
 
            if event.key == pygame.K_r and game_over: 
                reset_game() 
 
    keys = pygame.key.get_pressed() 
 
    if not game_over and not paused: 
        # Move player car 
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            player_x -= 6 
 
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            player_x += 6 
 
        if keys[pygame.K_UP] or keys[pygame.K_w]: 
            player_y -= 4 
 
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: 
            player_y += 4 
 
        # Keep car on the road 
        player_x = max( 
            ROAD_LEFT + 5, 
            min(player_x, ROAD_LEFT + ROAD_WIDTH - CAR_W - 5) 
        ) 
        player_y = max(80, min(player_y, HEIGHT - CAR_H - 10)) 
 
        # Move enemy car 
        enemy_y += speed 
 
        if enemy_y > HEIGHT: 
            enemy_y = -100 
            enemy_x = random.choice([ 
                ROAD_LEFT + 25, 
                ROAD_LEFT + LANE_WIDTH + 25, 
                ROAD_LEFT + 2 * LANE_WIDTH + 25 
            ]) 
            score += 1 
            speed = min(12, 5 + score // 5) 
 
        # Collision detection 
        player_rect = pygame.Rect( 
            player_x + 4, player_y + 4, CAR_W - 8, CAR_H - 8 
        ) 
        enemy_rect = pygame.Rect( 
            enemy_x + 4, enemy_y + 4, CAR_W - 8, CAR_H - 8 
        ) 
 
        if player_rect.colliderect(enemy_rect): 
            game_over = True 
 
        road_line_y = (road_line_y + speed) % 80 
 
    # Draw background 
    screen.fill(GREEN) 
 
    # Draw road 
    pygame.draw.rect( 
        screen, GRAY, 
        (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT) 
    ) 
 
    # Road borders 
    pygame.draw.rect( 
        screen, YELLOW, 
        (ROAD_LEFT, 0, 5, HEIGHT) 
    ) 
    pygame.draw.rect( 
        screen, YELLOW, 
        (ROAD_LEFT + ROAD_WIDTH - 5, 0, 5, HEIGHT) 
    ) 
 
    # Lane markings 
    for y in range(-80, HEIGHT, 80): 
        line_y = y + road_line_y 
 
        for lane in (1, 2): 
            x = ROAD_LEFT + lane * LANE_WIDTH 
            pygame.draw.rect( 
                screen, WHITE, 
                (x - 3, line_y, 6, 40) 
            ) 
 
    # Draw cars 
    draw_car(player_x, player_y, BLUE) 
    draw_car(enemy_x, enemy_y, RED) 
 
    # HUD 
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 65)) 
    screen.blit(font.render(f"Score: {score}", True, WHITE), (15, 15)) 
    screen.blit( 
        small_font.render(f"Speed: {speed}", True, YELLOW), 
        (350, 22) 
    ) 
 
    if paused: 
        screen.blit( 
            font.render("PAUSED", True, YELLOW), 
            (180, 300) 
        ) 
 
    if game_over: 
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) 
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0, 0)) 
 
        screen.blit( 
            font.render("GAME OVER!", True, RED), 
            (145, 270) 
        ) 
        screen.blit( 
            font.render(f"Score: {score}", True, WHITE), 
            (185, 315) 
        ) 
        screen.blit( 
            small_font.render("Press R to Restart", True, WHITE), 
            (165, 365) 
        ) 
 
    pygame.display.flip() 
 
pygame.quit() 
sys.exit()   
