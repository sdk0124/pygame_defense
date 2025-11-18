import pygame
import math

from core.settings import CELL_SIZE
from data.turret_data import TURRET_DATA


class Turret(pygame.sprite.Sprite):
    def __init__(self, tile_x, tile_y, turret_type, idle_image, attack_images):
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

        self.state = "idle" # 기본값 : 대기 상태

        self.idle_base_image = idle_image   # 대기 이미지
        self.attack_base_images = attack_images # 공격 이미지 (리스트)
        self.current_image = self.idle_base_image
        self.frame_speed = 0.08
        self.anim_timer = 0.0
        self.anim_idx = 0

        self.image = self.current_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.target = None

        self.time_since_last_shot = 0.0   # 마지막으로 공격한 시각

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

    def _try_attack(self, dt):
        """공격 쿨다운"""
        self.time_since_last_shot += dt

        attack_interval = 1.0 / self.fire_rate

        if self.time_since_last_shot >= attack_interval:
            self.time_since_last_shot -= attack_interval
            self.attack()

    def attack(self):
        """실제 공격 로직"""
        if self.target is None:
            return
        
        # 추후에 enemy class에 take_damage 메소드를 호출.
        pass

    def _update_animation(self, dt):
        """터렛의 상태에 따라 보여지는 이미지가 다르다"""
        # 대기 상태일 경우
        if self.state == "idle":
            self.current_image = self.idle_base_image
            self.anim_idx = 0
            self.anim_timer = 0.0
            return

        # 공격 상태일 경우
        self.anim_timer += dt * (1.0 / self.frame_speed)
        if self.anim_timer >= 1.0:
            self.anim_timer -= 1.0
            self.anim_idx += 1
            if self.anim_idx >= len(self.attack_base_images):
                self.anim_idx = 0
        
        self.current_image = self.attack_base_images[self.anim_idx]

    def update(self, dt, enemies):
        self._update_target(enemies)

        if self.target is not None:
            self._try_attack(dt)
            self.state = "attack"
        else:
            self.state = "idle"
        
        self._update_animation(dt)

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