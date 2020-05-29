import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


Name = """Alien Invasion"""

def run_game():
    """This is the main program of the game"""
    # init the game and create a screen object
    pygame.init()
    
    # create a settings
    ai_settings = Settings()

    screen = pygame.display.set_mode((
        ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption(Name)
    
    # create start button
    play_button = Button(ai_settings, screen, "Play")
    # create a game stats class
    stats = GameStats(ai_settings)
    # create a scoreboard
    scoreboard = Scoreboard(ai_settings, screen, stats)
    # create a Ship
    ship = Ship(ai_settings ,screen)
    # create a group of bullet
    bullets = Group()
    # create group of alien
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # start game main loop
    while True:
        
        # monitor mouse and keybroad
        gf.check_events(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets)

        if stats.game_active:
            # update ship movements
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
            # redraw screen
        
        gf.update_screen(ai_settings, stats, screen, ship, aliens, bullets, play_button, scoreboard)

run_game()