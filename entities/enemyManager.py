import pygame
from collections import deque
from entities.enemy import Enemy

class EnemyManager:
    def __init__(self, waypoints, enemy_data_table, enemy_image_table):
        self.waypoints = waypoints
        self.enemy_data_table = enemy_data_table
        self.image_table = enemy_image_table
        self.enemies = pygame.sprite.Group()

        self.wave_queue = deque()

        self.spawn_timer = 0

    def set_wave(self, cur_wave_idx, wave_data):
        """라운드 시작 시 만들어야 할 적 목록 세팅"""
        spawn_enemy_data = wave_data[cur_wave_idx]["enemies"]
        self.spawn_delay = wave_data[cur_wave_idx]["spawn_delay"]

        for enemy_type, count in spawn_enemy_data.items():
            for _ in range(count):
                self.wave_queue.append(enemy_type)
        
        print(self.wave_queue) # 체크용도
    
    def spwan_enemy(self):
        """매 스폰 주기마다 적 생성"""
        if (self.spawn_timer >= self.spawn_delay and len(self.wave_queue) != 0):
            enemy_type = self.wave_queue.popleft()
            enemy_data = self.enemy_data_table[enemy_type]
            new_enemy = Enemy(enemy_data, self.waypoints, self.image_table[enemy_type])
            self.enemies.add(new_enemy)
            self.spawn_timer = 0

    def update(self, dt):
        "모든 적 상태 갱신"
        self.spawn_timer += dt
        self.spwan_enemy()
    
        for enemy in self.enemies:
            enemy.move()
        
    def draw(self, surface):
        "모든 적 그리기"
        for enemy in self.enemies:
            enemy.draw(surface)
