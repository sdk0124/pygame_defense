# scenes/game_scene.py
import pygame

from resource_loader import load_map_image, load_map_data, load_enemy_images, load_turret_images
from entities.world import World
from entities.enemyManager import EnemyManager

from data.enemy_data import ENEMY_DATA
from data.wave_data import WAVE_DATA

from ui.sample_button import Button
from scenes.scene import Scene

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.score = 0
        self.money = 0
        self.current_round = 1
        self.wave_active = False
        self.wave_data = WAVE_DATA

        self.world = World(load_map_data(), load_map_image())
        self.world.process_data()

        self.enemy_manager = self.create_enemy_manager()

        # 임시 버튼 1 : 게임 오버 화면으로 이동
        self.end_button = Button(600, 400, 200, 60, "switch to Game Over")
        # 임시 버튼 2 : 라운드 시작
        self.round_start_btn = Button(800, 400, 200, 60, "Round Start!")

    def create_enemy_manager(self):
        """enemyManager 생성"""
        enemy_images = load_enemy_images()
        waypoints = self.world.get_waypoints()
        return EnemyManager(waypoints, ENEMY_DATA, enemy_images)

    def go_to_game_end(self):
        """게임 오버 화면으로 이동"""
        from scenes.end_scene import GameOverScene
        self.switch_to(GameOverScene(self.game, final_score=0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if self.end_button.handle_event(event):
                self.go_to_game_end()
                
            if not self.wave_active and self.round_start_btn.handle_event(event):
                """
                현재 웨이브가 비활성화 상태이고,
                그 때 유저가 '웨이브 시작' 버튼을 누르면 웨이브 생성
                """
                self.enemy_manager.set_wave(self.current_round - 1, self.wave_data)
                self.wave_active = True

    def update(self, dt):
        if self.wave_active:
            self.enemy_manager.update(dt)

            if self.enemy_manager.is_wave_done():
                self.wave_active = False
                print("웨이브 종료") # 확인용

    def draw(self, screen):
        self.world.draw(screen)

        if self.wave_active:
            self.enemy_manager.draw(screen)

        self.end_button.draw(screen)
        self.round_start_btn.draw(screen)