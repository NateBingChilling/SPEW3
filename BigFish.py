import pygame
from Fish import Fish
import random
import numpy as np

class BigFish(Fish):
    def __init__(self, parent1 = None, parent2 = None):
        self.state = ['search']
        super().__init__(parent1, parent2, 2400, 1.2, image='fishClipart2.png')
        self.reproduction_cooldown = 3000
        self.age = 11000

    def act(self, input):
        self.age -= 1
        self.hunger -= 1
        self.reproduction_cooldown -= 1
        self.update_state(input)
        match self.state[0]:
            case 'recenter':
                self.recenter()
            case 'player':
                self.player_control()
            case 'hunt':
                self.go()
            case 'mate':
                self.go()
            case 'search':
                self.search()

    def update_state(self, input):
        if self.rect.centerx < 20:
            self.state = ['recenter', 'right']
        elif self.rect.centerx > 780:
            self.state = ['recenter', 'left']
        elif self.rect.centery < 20:
            self.state = ['recenter', 'down']
        elif self.rect.centery > 580:
            self.state = ['recenter', 'up']
        else:
            nearest_prey = self.nearest(input[1])
            if self.hunger < 1600 and nearest_prey[0] < 400:
                self.target_dir = nearest_prey[1]
                self.state = ['hunt']
                return
            if self.reproduction_cooldown < 0:
                possible_mates = []
                for fish in input[2]:
                    if fish == self:
                        continue
                    elif fish.reproduction_cooldown < 0:
                        possible_mates.append(fish)
                nearest_mate = self.nearest(possible_mates)
                if nearest_mate[0] < 350:
                    self.target_dir = nearest_mate[1]
                    self.state = ['mate']
            else:
                self.state = ['search']

    def recenter(self):
        self.target_dir = random.random() * np.pi * 2
        match self.state[1]:
            case 'right':
                self.rect.centerx += self.speed
            case 'left':
                self.rect.centerx -= self.speed
            case 'down':
                self.rect.centery += self.speed
            case 'up':
                self.rect.centery -= self.speed

    def go(self):
        self.rect.centerx += self.speed * np.cos(self.target_dir)
        self.rect.centery += self.speed * np.sin(self.target_dir)

    def player_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.centerx -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.centerx += self.speed
        if keys[pygame.K_UP]:
            self.rect.centery -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.centery += self.speed

    def search(self):
        if random.random() < 0.03:
            self.target_dir = random.random() * np.pi * 2
        self.rect.centerx += self.speed * np.cos(self.target_dir)
        self.rect.centery += self.speed * np.sin(self.target_dir)