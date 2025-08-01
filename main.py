import pygame
import os
import sys
import random

# --- Grid & Screen Configuration ---
CELL_SIZE = 50
GRID_WIDTH = 15
GRID_HEIGHT = GRID_WIDTH # Make the grid square

# --- Color Definitions ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 80, 80)
DARK_GRAY = (100, 100, 100)

# --- Calculated Screen Dimensions ---
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# --- Pygame Initialization ---
os.environ['SDL_AUDIODRIVER'] = 'dsp'
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Click the Blue Square!")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 50)

# --- Game State and Variables ---
game_state = 'start_menu'
# The single blue square on the screen at any time
current_target = None 
red_flash_timer = 0
red_flash_pos = None

def set_new_target():
    """Finds a random new cell to be the next target."""
    global current_target
    old_target = current_target
    while True:
        new_col = random.randint(0, GRID_WIDTH - 1)
        new_row = random.randint(0, GRID_HEIGHT - 1)
        new_pos = (new_col, new_row)
        # Make sure the new target isn't the same as the old one
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
                # Check if the start button was clicked
                if start_button_rect.collidepoint(mouse_pos):
                    game_state = 'playing'
                    set_new_target() # Set the very first target

            elif game_state == 'playing':
                col = mouse_pos[0] // CELL_SIZE
                row = mouse_pos[1] // CELL_SIZE
                clicked_pos = (col, row)

                # Check for correct click
                if clicked_pos == current_target:
                    # The square turns white on the next frame's screen.fill()
                    set_new_target() # Immediately set a new target
                # Check for incorrect click
                else:
                    red_flash_pos = clicked_pos
                    red_flash_timer = 20 # Flash for 20 frames

    # --- Drawing Logic ---
    screen.fill(WHITE)

    if game_state == 'start_menu':
        # Draw Start Button
        button_width, button_height = 200, 80
        start_button_rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2, 
            (SCREEN_HEIGHT - button_height) // 2, 
            button_width, 
            button_height
        )
        pygame.draw.rect(screen, BLUE, start_button_rect, border_radius=15)
        start_text = font.render('Start', True, WHITE)
        text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, text_rect)

    elif game_state == 'playing':
        draw_grid()

        # Draw the current blue target square
        if current_target:
            draw_cell(current_target[0], current_target[1], BLUE)

        # Handle the red flash for wrong clicks
        if red_flash_timer > 0:
            # Make sure we don't draw red over the current blue target
            if red_flash_pos != current_target:
                draw_cell(red_flash_pos[0], red_flash_pos[1], RED)
            red_flash_timer -= 1

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
