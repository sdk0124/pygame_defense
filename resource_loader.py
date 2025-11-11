import pygame

def load_enemy_images():
    enemy_images = {
        "byter" : pygame.image.load("assets/images/enemy_byter.png").convert_alpha(),
        "worm" : pygame.image.load("assets/images/enemy_worm.png").convert_alpha(),
        "boss" : pygame.image.load("assets/images/enemy_byter.png").convert_alpha()
    }

    return enemy_images