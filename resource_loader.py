import pygame
import json

from core.settings import TURRET_ANIM_STEPS

def load_enemy_images():
    """적 이미지 불러오기"""
    enemy_images = {
        "byter" : pygame.image.load("assets/images/enemies/enemy_byter.png").convert_alpha(),
        "worm" : pygame.image.load("assets/images/enemies/enemy_worm.png").convert_alpha(),
        "boss" : pygame.image.load("assets/images/enemies/enemy_boss.png").convert_alpha()
    }

    return enemy_images

def split_spritesheet(spritesheet, frame_count):
        size = spritesheet.get_height()
        image_list = []

        for x in range(frame_count):
            temp_image = spritesheet.subsurface(x * size, 0, size, size)
            image_list.append(temp_image)

        return image_list

def load_turret_images():
    """터렛 이미지 불러오기"""
    """idle 이미지 : 1장 / attack 이미지 : 여러 장이므로 주의"""
    turret_images = {
        "cannon" : {
            "idle" : pygame.image.load("assets/images/turrets/cannon.png").convert_alpha(),
            "attack" : split_spritesheet(pygame.image.load("assets/images/turrets/cannon_attack.png").convert_alpha(),
                TURRET_ANIM_STEPS)
        },
        "debugger" : {
            "idle" : pygame.image.load("assets/images/turrets/core_debugger.png").convert_alpha(),
            "attack" : split_spritesheet(pygame.image.load("assets/images/turrets/core_debugger_attack.png").convert_alpha(),
                TURRET_ANIM_STEPS)
        }
    }

    return turret_images

def load_map_image():
    """맵 타일 이미지 불러오기"""
    map_image = pygame.image.load("assets/images/map/round_map.png").convert_alpha()
    
    return map_image

def load_map_data():
    """맵 데이터 불러오기"""
    with open('data/round_map.tmj') as file:
        world_data = json.load(file)

    return world_data

def load_final_base_image():
    """최종 방어선 (CPU) 이미지 불러오기"""
    final_base_image = pygame.image.load("assets/images/final_base/round_map.png").convert_alpha()

    return final_base_image