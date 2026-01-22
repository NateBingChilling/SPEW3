import random
import pygame
import numpy as np

class Fish(pygame.sprite.Sprite):
    def __init__(self, parent1 = None, parent2 = None, hunger = 600, speed = 4, image = 'fishClipart2.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        if not (parent1 is None or parent2 is None):
            self.rect.centerx = (parent1.rect.centerx + parent2.rect.centerx)//2
            self.rect.centery = (parent1.rect.centery + parent2.rect.centery) // 2
        else:
            self.rect.centerx = random.randrange(100, 700)
            self.rect.centery = random.randrange(100, 500)
        self.hunger = hunger
        self.speed = speed
        self.age = 6000
        self.reproduction_cooldown = 1200
        self.target_dir = 0


    def act(self, input):
        pass

    def dist_dir(self, target):
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        return np.sqrt(dx ** 2 + dy ** 2), np.arctan2(dy, dx)

    def nearest(self, arr):
        min_dist = 1000000
        stored_dir = 0
        for target in arr:
            dist, direction = self.dist_dir(target)
            if dist < min_dist:
                min_dist = dist
                stored_dir = direction
        return min_dist, stored_dir