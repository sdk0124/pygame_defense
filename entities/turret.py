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

        self.is_attack_anim_playing = False # 공격 애니메이션 재생 여부
        self.attack_anim_time = 0.0 # 공격 애니메이션 경과 시간
        self.attack_anim_total_time = 0.3   # 공격 애니메이션 재생 총 길이(초)

        self.angle = 0

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
        """
        스티키 타겟팅 : 
        한 번 적이 범위 내로 들어오면 죽거나 범위 밖을 나갈 때까지 변화 X
        """
        range_sq = self.range * self.range

        # 현재 타겟이 유효하면 그대로 유지
        if self.target is not None:
            # 타겟이 아직 살아있고 사거리 안에 있으면 그대로 둔다.
            if self.target.alive() and (self._distance_sq(self.target) <= self.range * self.range):
                # print("타겟이 있습니다.")
                return
            # 그렇지 않으면 타겟 해제
            self.target = None

        # 타겟이 없으면 새로 탐색
        # print("타겟이 없습니다..")
        nearest = None
        nearest_dist_sq = range_sq

        for enemy in enemies:
            # enemy가 죽었으면 스킵
            if not enemy.alive():
                continue

            # 사거리 안에 들어온 적들이 후보
            dist_sq = self._distance_sq(enemy)
            if dist_sq <= range_sq and (nearest is None or dist_sq < nearest_dist_sq):
                nearest = enemy
                nearest_dist_sq = dist_sq

        # 새 타겟 설정 (없으면 None 유지됨.)
        self.target = nearest
    
    def _distance_sq(self, enemy):
        """터렛과 적과의 거리 계산"""
        dx = enemy.position.x - self.x
        dy = enemy.position.y - self.y
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
        
        self.target.take_damage(self.damage)
        print("터렛이 공격했습니다.")
        
        self.is_attack_anim_playing = True
        self.attack_anim_time = 0.0
        self.anim_idx = 0

    def _update_animation(self, dt):
        """터렛의 상태에 따라 재생하는 이미지 설정"""
        # 1 : 공격 상태일 때
        if self.is_attack_anim_playing:
            self.attack_anim_time += dt

            frame_count = len(self.attack_base_images)
            if frame_count == 0:
                # 혹시 리스트 비어 있으면 그냥 종료
                self.is_attack_anim_playing = False
                self.current_image = self.idle_base_image
                return

            # 한 번 공격 애니메이션 전체 길이 (원하는 값으로 조절)
            frame_time = self.attack_anim_total_time / frame_count

            # 현재 시간이 몇 번째 프레임인지
            self.anim_idx = int(self.attack_anim_time / frame_time)
            # print(self.anim_idx) # 테스트용

            if self.anim_idx >= frame_count:
                # 애니메이션 끝 -> idle로 복귀
                self.is_attack_anim_playing = False
                self.current_image = self.idle_base_image
                self.anim_idx = 0
                return

            # 아직 애니메이션 진행 중이면 해당 프레임 사용
            self.current_image = self.attack_base_images[self.anim_idx]
            return

        # 2 : 공격 애니메이션이 재생 중이 아닐 때 = 항상 idle 이미지
        self.current_image = self.idle_base_image

    def _rotate_to_target(self):
        """타겟 위치에 따라 터렛 회전"""
        if self.target is None:
            return
        
        tx, ty = self.target.position.x, self.target.position.y
        dx = tx - self.x
        dy = ty - self.y

        angle_rad = math.atan2(dy, dx)
        self.angle = math.degrees(angle_rad)

    def _update_image_by_rotation(self):
        rotated_image = pygame.transform.rotate(self.current_image, -self.angle)

        old_center = self.rect.center
        self.image = rotated_image
        self.rect = self.image.get_rect(center=old_center)

    def update(self, dt, enemies):
        self._update_target(enemies)

        if self.target is not None:
            self._rotate_to_target()
            self.state = "attack"
        else:
            self.state = "idle"
        
        self._try_attack(dt)
        self._update_animation(dt)
        self._update_image_by_rotation()

    def draw(self, surface):
        """터렛 그리기"""
        self.draw_range(surface)
        surface.blit(self.image, self.rect)

### 테스트 코드 ###
if __name__ == "__main__":

    from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    from resource_loader import load_enemy_images, load_map_data, load_map_image, load_turret_images
    
    from entities.enemyManager import EnemyManager
    from entities.world import World

    from data.enemy_data import ENEMY_DATA
    from data.wave_data import WAVE_DATA

    ### 임시 함수 및 임시 상수 ###

    TURRET_ANIM_STEPS = 6

    def set_attack_images(attack_spritesheet):
        size = attack_spritesheet.get_height()
        attack_images = []

        for x in range(TURRET_ANIM_STEPS):
            temp_image = attack_spritesheet.subsurface(x * size, 0, size, size)
            attack_images.append(temp_image)

        return attack_images

    ### 임시 함수 및 임시 상수 끝 ###


    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    world = World(load_map_data(), load_map_image())
    world.process_data()

    enemy_images = load_enemy_images()
    turret_images = load_turret_images()

    cannon_attack_images = set_attack_images(turret_images["cannon"]["attack"])
    debugger_attack_images = set_attack_images(turret_images["debugger"]["attack"])

    # print(len(debugger_attack_images))

    new_cannon = Turret(4, 5, "cannon", turret_images["cannon"]["idle"], cannon_attack_images)
    new_debugger = Turret(4, 10, "debugger", turret_images["debugger"]["idle"], debugger_attack_images)

    new_cannon.fire_rate = 0.5 # 임시로 수정
    new_debugger.fire_rate = 0.25 # 임시로 수정

    new_debugger.range = 400 # 임시로 수정

    cur_wave_round = 3
    wave_data = WAVE_DATA

    enemy_manager = EnemyManager(world.get_waypoints(), ENEMY_DATA, enemy_images)
    enemy_manager.set_wave(cur_wave_round - 1, wave_data)

    running = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.draw(screen)

        enemy_manager.update(dt)
        
        new_cannon.update(dt / 1000, enemy_manager.enemies)
        new_debugger.update(dt / 1000, enemy_manager.enemies)

        enemy_manager.draw(screen)
        new_cannon.draw(screen)
        new_debugger.draw(screen)
        pygame.display.flip()
    
    pygame.quit()