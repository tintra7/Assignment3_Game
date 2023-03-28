import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# # Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Star Screen")

# Define font
font = pygame.font.Font(None, 36)

# Define menu items
menu_items = [
    "Start",
    "Options",
    "Exit"
]

# Define menu item rectangles
menu_item_rects = []
for i, item in enumerate(menu_items):
    item_rect = pygame.Rect(0, 0, 200, 50)
    item_rect.center = (screen_width // 2, screen_height // 2 + i * 75)
    menu_item_rects.append(item_rect)

# Define star class
class Star:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y += self.speed
        if self.y > screen_height:
            self.y = -10
            self.x = random.randint(0, screen_width)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 2)

# Define list of stars
stars = []
for i in range(100):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    speed = random.randint(1, 5)
    star = Star(x, y, speed)
    stars.append(star)

# Define function to draw stars
def draw_stars():
    for star in stars:
        star.move()
        star.draw()

# Main game loop
menu_screen = True
game_screen = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            # Check if a menu item was clicked
            for i, item_rect in enumerate(menu_item_rects):
                if item_rect.collidepoint(event.pos):
                    if i == 0:
                        menu_screen = False
                        game_screen = True
                    elif i == 1:
                        print("Opening options menu...")
                    elif i == 2:
                        running = False

    if menu_screen:
        # Draw the menu items
        screen.fill(BLACK)
        for i, item in enumerate(menu_items):
            item_surface = font.render(item, True, WHITE)
            item_rect = item_surface.get_rect()
            item_rect.center = menu_item_rects[i].center
            screen.blit(item_surface, item_rect)
    elif game_screen:
        # Draw the star screen
        screen.fill(BLACK)
        draw_stars()
        text_surface = font.render("Press ESC to return to menu", True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_width // 2, screen_height - 50)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

    # Check for ESC key press to return to menu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        menu_screen = True
        game_screen = False

# Clean up
pygame.quit()