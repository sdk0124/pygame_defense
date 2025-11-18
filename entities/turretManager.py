import pygame
from entities.turret import Turret
from core.settings import CELL_SIZE

class TurretManager:
    def __init__(self, world_tilemap, turret_data_table, turret_image_table):
        self.world_tilemap = world_tilemap
        self.turret_data_table = turret_data_table
        self.turret_image_table = turret_image_table
        self.turrets = pygame.sprite.Group()

    def create_turret(self, mouse_pos, tile_size, col, turret_type):
        """해당 타일에 터렛 설치"""
        grid_x = mouse_pos[0] // tile_size
        grid_y = mouse_pos[0] // tile_size

        mouse_tile_num = (grid_y * col) + grid_x

        # 41 : 타일맵에서 길이 아닌 곳을 의미.
        if self.world_tilemap[mouse_tile_num] == 41:
            for turret in self.turrets:
                # 이미 설치된 곳은 설치하면 안됨.
                if (grid_x, grid_y) == (turret.tile_x, turret.tile_y):
                    return
            
            turret_data = self.turret_data_table[turret_type]
            turret_idle_image = self.turret_image_table[turret_type]["idle"]
            turret_attack_images = self.turret_image_table[turret_type]["attack"]
            
            new_turret = Turret(grid_x, grid_y,
                                CELL_SIZE,
                                turret_data,
                                turret_idle_image,
                                turret_attack_images)
            
            self.turrets.add(new_turret)

            print(f"터렛이 설치됨: ({grid_x}, {grid_y})") # 테스트용

    def update(self, dt, enemies):
        for turret in self.turrets:
            turret.update(dt, enemies)
    
    def draw(self, surface):
        for turret in self.turrets:
            turret.draw(surface)