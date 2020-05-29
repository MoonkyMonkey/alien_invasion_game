import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """alien class"""

    def __init__(self, ai_settings, screen):
        """init alien and set start positions"""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # load alien image and set rect attr
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # set the initial position
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # acculate position
        self.x = float(self.rect.x)

    def check_edges(self):
        """if alien in edge of screen return true"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """move alien to right"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """draw alien in screen"""
        self.screen.blit(self.image, self.rect)