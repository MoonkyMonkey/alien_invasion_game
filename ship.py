import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """This class define a ship"""

    def __init__(self, ai_settings, screen):
        super().__init__()
        """initial the ship and settings start position"""
        self.screen = screen
        self.ai_settings = ai_settings
        
        # load ship picture
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # set to center of the button
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        # move flags
        self.moving_right = False
        self.moving_left = False
        # self.moving_down = False
        # self.moving_up = False

    def update(self):
        """update movements by moving flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        # update rect by self.centerx
        self.rect.centerx = self.center
        

    def blitme(self):
        """draw ship in specific location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """let ship back to center"""
        self.center = self.screen_rect.centerx