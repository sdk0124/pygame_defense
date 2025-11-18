import pygame
import math

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

        self.target = None

    def draw_range(self, surface):
        """터렛 범위를 원 모양으로 그리기"""
        range_surf = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(range_surf, "grey100", (self.range, self.range), self.range)
        range_surf.set_alpha(100)
        range_rect = range_surf.get_rect()
        range_rect.center = (self.x, self.y)

        surface.blit(range_surf, range_rect)

    def _update_target(self, enemies):
        """터렛의 가장 가까운 타겟 적 업데이트"""
        if self.target is not None:
            if (not self.target.alive()) or (self._distance_sq(self.target) > self.range * self.range):
                self.target = None

        if self.target is None:
            nearest = None
            nearest_dist_sq = None

            for enemy in enemies:
                # enemy가 죽었으면 스킵
                if not enemy.alive():
                    continue

                dist_sq = self._distance_sq(enemy)
                if dist_sq <= self.range * self.range:
                    if nearest is None or dist_sq < nearest_dist_sq:
                        nearest = enemy
                        nearest_dist_sq = dist_sq

            self.target = nearest
    
    def _distance_sq(self, enemy):
        """터렛과 적과의 거리 계산"""
        dx = enemy.position[0] - self.x
        dy = enemy.position[1] - self.y
        return (dx * dx) + (dy * dy)         

    def draw(self, surface):
        """터렛 그리기"""
        self.draw_range(surface)
        surface.blit(self.image, self.rect)

### 테스트 코드 ###
if __name__ == "__main__":

    from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    from resource_loader import load_enemy_images, load_map_data, load_map_image, load_turret_images

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    map_image = load_map_image()
    map_data = load_map_data()
    enemy_images = load_enemy_images()

    turret_images = load_turret_images()

    new_cannon = Turret(4, 5, "cannon", turret_images["cannon"]["idle"])
    new_debugger = Turret(4, 10, "debugger", turret_images["debugger"]["idle"])

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(map_image, (0, 0))
        new_cannon.draw(screen)
        new_debugger.draw(screen)
        pygame.display.flip()
    
    pygame.quit()