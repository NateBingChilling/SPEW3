import pygame
import random

class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Food.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(10, 790)
        self.rect.centery = -18
        self.speed = 1

    def move(self):
        self.rect.centery += self.speed