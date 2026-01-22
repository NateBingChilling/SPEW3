from Fish import Fish
import pygame
import random
import numpy as np


# States: search, eat, flee, mate
class SmallFish(Fish):
    def __init__(self, parent1=None, parent2=None):
        self.state = ['search']
        super().__init__(parent1, parent2, 800, 2.8, image='TinyFish.jpg')
        self.reproduction_cooldown = 600
        self.age = 3000

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
            case 'run':
                self.go()
            case 'eat':
                self.go()
            case 'mate':
                self.go()
            case 'search':
                self.search()

    def update_state(self, input):
        if self.rect.centerx < 10:
            self.state = ['recenter', 'right']
        elif self.rect.centerx > 790:
            self.state = ['recenter', 'left']
        elif self.rect.centery < 10:
            self.state = ['recenter', 'down']
        elif self.rect.centery > 590:
            self.state = ['recenter', 'up']
        else:
            nearest_predator = self.nearest(input[2])
            if nearest_predator[0] < 100:
                self.target_dir = np.pi + nearest_predator[1]
                self.state = ['run']
                return
            nearest_food = self.nearest(input[0])
            if self.hunger < 400 and nearest_food[0] < 150:
                self.target_dir = nearest_food[1]
                self.state = ['eat']
                return
            if self.reproduction_cooldown < 0:
                possible_mates = []
                for fish in input[1]:
                    if fish == self:
                        continue
                    elif fish.reproduction_cooldown < 0:
                        possible_mates.append(fish)
                nearest_mate = self.nearest(possible_mates)
                if nearest_mate[0] < 200:
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
        if random.random() < 0.1:
            self.target_dir = random.random() * np.pi * 2
        self.rect.centerx += self.speed * np.cos(self.target_dir)
        self.rect.centery += self.speed * np.sin(self.target_dir)