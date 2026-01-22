import pygame
import sys
import numpy as np

from BigFish import BigFish
from SmallFish import SmallFish
from Food import Food

def dist_dir(obj1, obj2):
    dx = obj2.rect.centerx - obj1.rect.centerx
    dy = obj2.rect.centery - obj1.rect.centery
    return np.sqrt(dx ** 2 + dy ** 2), np.arctan2(dy, dx)

def kill_time(fish_arr):
    for fish in fish_arr:
        if fish.hunger <= 0 or fish.age <= 0:
            fish_arr.remove(fish)
            del fish

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Image")
clock = pygame.time.Clock()

small_fish_arr = [SmallFish() for _ in range(10)]
big_fish_arr = [BigFish() for _ in range(3)]

food_arr = []
food_frame_count = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((180, 190, 250))
    food_frame_count += 1
    if food_frame_count > 16:
        food_frame_count = 0
        food_arr.append(Food())

    for food in food_arr:
        food.move()
        if food.rect.centery>610:
            food_arr.remove(food)
            del food
            break
        screen.blit(food.image, food.rect)

    for small_fish in small_fish_arr:
        small_fish.act([food_arr, small_fish_arr, big_fish_arr])

    for big_fish in big_fish_arr:
        big_fish.act([food_arr, small_fish_arr, big_fish_arr])

    for small_fish in small_fish_arr:
        for food in food_arr:
            if small_fish.hunger < 400 and pygame.sprite.collide_circle(small_fish, food):
                food_arr.remove(food)
                del food
                small_fish.hunger = 800

    for small_fish_1 in small_fish_arr:
        for small_fish_2 in small_fish_arr:
            if small_fish_1 == small_fish_2:
                continue
            elif small_fish_1.reproduction_cooldown < 0 and small_fish_2.reproduction_cooldown < 0 and pygame.sprite.collide_circle(small_fish_1, small_fish_2):
                small_fish_arr.append(SmallFish(parent1 = small_fish_1, parent2 = small_fish_2))
                small_fish_1.reproduction_cooldown = 600
                small_fish_2.reproduction_cooldown = 600

    for big_fish_1 in big_fish_arr:
        for big_fish_2 in big_fish_arr:
            if big_fish_1 == big_fish_2:
                continue
            elif big_fish_1.reproduction_cooldown < 0 and big_fish_2.reproduction_cooldown < 0 and pygame.sprite.collide_circle(big_fish_1, big_fish_2):
                big_fish_arr.append(BigFish(parent1 = big_fish_1, parent2 = big_fish_2))
                big_fish_1.reproduction_cooldown = 3200
                big_fish_2.reproduction_cooldown = 3200

    for big_fish in big_fish_arr:
        for small_fish in small_fish_arr:
            if big_fish.hunger < 1600 and pygame.sprite.collide_circle(big_fish, small_fish):
                small_fish_arr.remove(small_fish)
                del small_fish
                big_fish.hunger = 2400

    kill_time(small_fish_arr)
    kill_time(big_fish_arr)

    for small_fish in small_fish_arr:
        # Draw image
        screen.blit(small_fish.image, small_fish.rect)

    for big_fish in big_fish_arr:
        # Draw image
        screen.blit(big_fish.image, big_fish.rect)

    # Update display
    pygame.display.flip()

    # Limit FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
