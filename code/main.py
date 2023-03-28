import pygame
import sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):

        # game attributes
        self.max_level = 2
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # audio
        self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
        self.overworld_bg_music = pygame.mixer.Sound(
            '../audio/overworld_music.wav')

        # overworld creation
        self.overworld = Overworld(
            0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)

        # user interface
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld,
                           self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(
            current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)
        self.level_bg_music.stop()

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(
                0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops=-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()
        clock.tick(60)


# Pygame setup
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# # Set up the screen
# screen_width = 800
# screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Star Screen")

# Define font
font = pygame.font.Font(None, 36)

# Define menu items
menu_items = [
    "Start",
    "About",
    "Exit"
]

# Define menu item rectangles
menu_item_rects = []
for i, item in enumerate(menu_items):
    item_rect = pygame.Rect(0, 0, 200, 50)
    item_rect.center = (screen_width // 2, screen_height // 2 + i * 75)
    menu_item_rects.append(item_rect)
background = pygame.image.load("../graphics/decoration/Background_01.png")
about_screen_img = pygame.image.load("../graphics/decoration/About.png")
clock = pygame.time.Clock()

game = Game()

menu_screen = True
game_screen = False
about_screen = False
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
                        menu_screen = False
                        game_screen = False
                        about_screen = True
                    elif i == 2:
                        running = False

    if menu_screen:
        # Draw the menu items
        screen.blit(background, (0, 0))
        for i, item in enumerate(menu_items):
            item_surface = font.render(item, True, WHITE)
            item_rect = item_surface.get_rect()
            item_rect.center = menu_item_rects[i].center
            screen.blit(item_surface, item_rect)

    if about_screen:

        screen.blit(about_screen_img, (0, 0))
    if game_screen:
        # Draw the star screen
        screen.blit(background, (0, 0))
        game.run()

        # text_surface = font.render("Press ESC to return to menu", True, YELLOW)
        # text_rect = text_surface.get_rect()
        # text_rect.center = (screen_width // 2, screen_height - 50)
        # screen.blit(text_surface, text_rect)

    pygame.display.flip()

    # Check for ESC key press to return to menu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        menu_screen = True
        about_screen = False
        game_screen = False


# Clean up
pygame.quit()