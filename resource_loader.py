import pygame
import json

def load_enemy_images():
    """적 이미지 불러오기"""
    enemy_images = {
        "byter" : pygame.image.load("assets/images/enemies/enemy_byter.png").convert_alpha(),
        "worm" : pygame.image.load("assets/images/enemies/enemy_worm.png").convert_alpha(),
        "boss" : pygame.image.load("assets/images/enemies/enemy_byter.png").convert_alpha()
    }

    return enemy_images

def load_map_image():
    """맵 타일 이미지 불러오기"""
    map_image = pygame.image.load("assets/images/map/round_map.png").convert_alpha()
    
    return map_image

def load_map_data():
    """맵 데이터 불러오기"""
    with open('data/round_map.tmj') as file:
        world_data = json.load(file)

    return world_data