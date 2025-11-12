import pygame
from core.settings import CELL_SIZE
from data.turret_data import TURRET_DATA

class Turret(pygame.sprite.Sprite):
    def __init__(self, tile_x, tile_y, turret_type, idle_image):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (tile_x + 0.5) * CELL_SIZE
        self.y = (tile_y + 0.5) * CELL_SIZE

        data = TURRET_DATA[turret_type]
        self.damage = data["damage"]
        self.range = data["range"]
        self.fire_rate = data["fire_rate"]
        self.purchase_price = data["purchase_price"]
        self.sell_price = data["sell_price"]

        self.image = idle_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    
    def draw(self, surface):
        """터렛 그리기"""
        surface.blit(self.image, self.rect)