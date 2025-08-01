import pygame
import os
import sys

# --- Grid & Screen Configuration ---
# Feel free to change these three variables to see how the grid changes.
CELL_SIZE = 40  # The size of each square in pixels
GRID_WIDTH = 20 # The number of squares wide the grid will be
GRID_HEIGHT = GRID_WIDTH # The number of squares high, set to width to make it square

# --- Color Definitions ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# --- Calculated Screen Dimensions ---
# The screen size is determined by the grid settings above.
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# --- Pygame Initialization ---
# This part sets up the Pygame environment on Replit.
os.environ['SDL_AUDIODRIVER'] = 'dsp' # Required for audio on Replit
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Easy-to-Change Grid")
clock = pygame.time.Clock()

def draw_grid():
    """
    Draws the grid lines onto the screen based on the configuration variables.
    """
    # Draw vertical lines
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))

    # Draw horizontal lines
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

# --- Main Game Loop ---
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing
    screen.fill(WHITE) # Fill the background with white
    draw_grid()        # Draw the grid lines on top of the background

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
