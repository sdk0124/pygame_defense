import pygame
from collections import deque
from entities.enemy import Enemy

class EnemyManager:
    def __init__(self, waypoints, enemy_data_table, enemy_image_table, on_enemy_death=None):
        self.waypoints = waypoints
        self.enemy_data_table = enemy_data_table
        self.image_table = enemy_image_table
        self.enemies = pygame.sprite.Group()
        self.on_enemy_death = on_enemy_death

        self.wave_queue = deque()

        self.spawn_timer = 0

    def set_wave(self, cur_wave_idx, wave_data):
        """라운드 시작 시 만들어야 할 적 목록 세팅"""
        self.spawn_timer = 0
        self.wave_queue.clear()
        self.enemies.empty()
    
        spawn_enemy_data = wave_data[cur_wave_idx]["enemies"]
        self.spawn_delay = wave_data[cur_wave_idx]["spawn_delay"]

        for enemy_type, count in spawn_enemy_data.items():
            for _ in range(count):
                self.wave_queue.append(enemy_type)
        
        print(self.wave_queue) # 체크용도
    
    def is_wave_done(self):
        """더 이상 생성할 적도 없고, 살아있는 적도 없는지 확인"""
        return not self.wave_queue and len(self.enemies) == 0

    def spwan_enemy(self):
        """매 스폰 주기마다 적 생성"""
        while self.spawn_timer >= self.spawn_delay and len(self.wave_queue) != 0:
            enemy_type = self.wave_queue.popleft()
            enemy_data = self.enemy_data_table[enemy_type]

            new_enemy = Enemy(enemy_data, 
                              self.waypoints, 
                              self.image_table[enemy_type], 
                              on_death=self.on_enemy_death)
            
            self.enemies.add(new_enemy)

            self.spawn_timer -= self.spawn_delay
            print(len(self.wave_queue)) # 확인용

    def update(self, dt, final_base):
        "모든 적 상태 갱신"
        self.spawn_timer += dt
        self.spwan_enemy()
    
        for enemy in self.enemies:
            enemy.update(dt, final_base)
        
    def draw(self, surface):
        "모든 적 그리기"
        for enemy in self.enemies:
            enemy.draw(surface)

### 테스트 코드 ###
if __name__ == "__main__":

    from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    from resource_loader import load_enemy_images, load_map_data, load_map_image

    #### 임시 함수 시작 #####
    points = []

    def process_data(map_data):
        # look through data to extract info
        for layer in map_data["layers"]:
            if layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    process_waypoints(obj)

    def process_waypoints(data):
        # iterate through waypoints to extract x, y
        x = data['x']
        y = data['y']
        points.append((x, y))

    #### 임시 함수 끝 #####

    #### 임시 import ####
    from data.wave_data import WAVE_DATA
    from data.enemy_data import ENEMY_DATA
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    map_image = load_map_image()
    map_data = load_map_data()
    enemy_images = load_enemy_images()
    process_data(map_data)

    print(points)

    running = True

    round_level = 3

    enemy_manager = EnemyManager(points, ENEMY_DATA, enemy_images)
    enemy_manager.set_wave(round_level - 1, WAVE_DATA)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(map_image, (0, 0))
        enemy_manager.update(FPS)
        enemy_manager.draw(screen)
        pygame.display.flip()
    
    pygame.quit()