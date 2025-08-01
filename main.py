import pygame
import os
import sys
import random
import math

# --- Grid & Screen Configuration ---
CELL_SIZE = 50
GRID_WIDTH = 15
GRID_HEIGHT = GRID_WIDTH # Make the grid square

# --- Game Constants ---
GAME_DURATION = 60 # Seconds

# --- Color Definitions ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 80, 80)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 200, 100)

# --- Calculated Screen Dimensions ---
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# --- Pygame Initialization ---
os.environ['SDL_AUDIODRIVER'] = 'dsp'
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Click the Blue Square!")
clock = pygame.time.Clock()
main_font = pygame.font.SysFont('Arial', 50)
score_font = pygame.font.SysFont('Arial', 30)

# --- Game State and Variables ---
game_state = 'start_menu'
current_target = None 
red_flash_timer = 0
red_flash_pos = None

# Score and Time variables
correct_clicks = 0
incorrect_clicks = 0
start_time = 0
final_bps = 0

def calculate_bps(Sc, Si, t, N):
    """Calculates BPS score using the provided formula."""
    if N <= 1 or t <= 0:
        return 0.0

    # BPS = max(0, log2(N - 1) * (Sc - Si) / t)
    term1 = math.log2(N - 1)
    term2 = (Sc - Si) / t
    score = term1 * term2

    return max(0, score)

def set_new_target():
    """Finds a random new cell to be the next target."""
    global current_target
    old_target = current_target
    while True:
        new_col = random.randint(0, GRID_WIDTH - 1)
        new_row = random.randint(0, GRID_HEIGHT - 1)
        new_pos = (new_col, new_row)
        if new_pos != old_target:
            current_target = new_pos
            break

def draw_grid():
    """Draws the grid lines onto the screen."""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

def draw_cell(col, row, color):
    """Draws a colored rectangle in a specific grid cell."""
    pygame.draw.rect(screen, color, (col * CELL_SIZE + 1, row * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1))

# --- Main Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if game_state == 'start_menu':
                if start_button_rect.collidepoint(mouse_pos):
                    game_state = 'playing'
                    correct_clicks = 0
                    incorrect_clicks = 0
                    start_time = pygame.time.get_ticks()
                    set_new_target()

            elif game_state == 'game_over':
                if play_again_button_rect.collidepoint(mouse_pos):
                    game_state = 'start_menu'

            elif game_state == 'playing':
                col = mouse_pos[0] // CELL_SIZE
                row = mouse_pos[1] // CELL_SIZE
                clicked_pos = (col, row)

                if clicked_pos == current_target:
                    correct_clicks += 1
                    set_new_target()
                else:
                    incorrect_clicks += 1
                    red_flash_pos = clicked_pos
                    red_flash_timer = 20

    # --- Game Logic & State Changes ---
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    if game_state == 'playing' and elapsed_time >= GAME_DURATION:
        game_state = 'game_over'
        grid_size_N = GRID_WIDTH * GRID_HEIGHT
        final_bps = calculate_bps(correct_clicks, incorrect_clicks, GAME_DURATION, grid_size_N)

    # --- Drawing Logic ---
    screen.fill(WHITE)

    if game_state == 'start_menu':
        button_width, button_height = 200, 80
        start_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, (SCREEN_HEIGHT - button_height) // 2, button_width, button_height)
        pygame.draw.rect(screen, BLUE, start_button_rect, border_radius=15)
        start_text = main_font.render('Start', True, WHITE)
        text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, text_rect)

    elif game_state == 'game_over':
        # Display final score
        title_text = main_font.render("Time's Up!", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title_text, title_rect)

        score_text = score_font.render(f"Final BPS: {final_bps:.2f}", True, DARK_GRAY)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        screen.blit(score_text, score_rect)

        # Play Again Button
        button_width, button_height = 250, 80
        play_again_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 50, button_width, button_height)
        pygame.draw.rect(screen, GREEN, play_again_button_rect, border_radius=15)
        play_again_text = main_font.render('Play Again', True, WHITE)
        play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
        screen.blit(play_again_text, play_again_text_rect)

    elif game_state == 'playing':
        draw_grid()

        if current_target:
            draw_cell(current_target[0], current_target[1], BLUE)

        if red_flash_timer > 0:
            if red_flash_pos != current_target:
                draw_cell(red_flash_pos[0], red_flash_pos[1], RED)
            red_flash_timer -= 1

        # Display HUD (Heads-Up Display)
        time_remaining = max(0, GAME_DURATION - elapsed_time)
        timer_text = score_font.render(f"Time: {time_remaining:.1f}", True, BLACK)
        screen.blit(timer_text, (10, 10))

        # Calculate and display BPS score in real-time
        grid_size_N = GRID_WIDTH * GRID_HEIGHT
        current_bps = calculate_bps(correct_clicks, incorrect_clicks, elapsed_time, grid_size_N)
        bps_text = score_font.render(f"BPS: {current_bps:.2f}", True, BLACK)
        bps_rect = bps_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(bps_text, bps_rect)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
