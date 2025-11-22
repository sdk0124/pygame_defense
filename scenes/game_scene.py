# scenes/game_scene.py
import pygame

from resource_loader import load_map_image, load_map_data, load_enemy_images, load_turret_images
from entities.world import World
from entities.enemyManager import EnemyManager

from data.enemy_data import ENEMY_DATA
from data.wave_data import WAVE_DATA

from ui.ui_manager import UIManager
from ui.image_button import ImageButton
from ui.label import Label
from core.settings import INFO_UI_PATH_CORE_DEBUGGER, INFO_UI_PATH_CANNON, UI_PATH_GAME_SCENE, UI_PATH_HP, UI_PATH_MONEY, UI_PATH_ROUND
from scenes.scene import Scene

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.info = {
            "money": 0,
            "hp": 10,
            "score": 0,
            "current_round": 1
        }
        self.wave_active = False
        self.wave_data = WAVE_DATA

        self.world = World(load_map_data(), load_map_image())
        self.world.process_data()

        self.enemy_manager = self.create_enemy_manager()

        # ui 준비
        self.prepare_uis()

    def create_enemy_manager(self):
        """enemyManager 생성"""
        enemy_images = load_enemy_images()
        waypoints = self.world.get_waypoints()
        return EnemyManager(waypoints, ENEMY_DATA, enemy_images)

    # 버튼 눌리면 호출할 함수
    def start_wave(self):
        """
        현재 웨이브가 비활성화 상태이고,
        그 때 유저가 '웨이브 시작' 버튼을 누르면 웨이브 생성
        """
        if not self.wave_active:
            self.enemy_manager.set_wave(self.info["current_round"] - 1, self.wave_data)
            self.wave_active = True

    # 버튼 눌리면 호출할 함수
    def go_to_game_end(self):
        """게임 오버 화면으로 이동"""
        from scenes.end_scene import GameOverScene
        self.switch_to(GameOverScene(self.game, final_score=0))
    
    # 터렛 선택
    def select_turret_cannon(self):
        self.selected_turret_info_uis = self.cannon_info_uis

    # 터렛 선택
    def select_turret_core_debugger(self):
        self.selected_turret_info_uis = self.core_debugger_info_uis

    # ui manager 생성
    def prepare_uis(self) -> UIManager:
        self.cannon_info_uis = UIManager()
        self.cannon_info_uis.load_uis(INFO_UI_PATH_CANNON)
        self.core_debugger_info_uis = UIManager()
        self.core_debugger_info_uis.load_uis(INFO_UI_PATH_CORE_DEBUGGER)
        self.uis = UIManager()
        self.uis.load_uis(
            UI_PATH_GAME_SCENE,
            {
                "start_wave": self.start_wave,
                "go_to_game_end": self.go_to_game_end,
                "select_turret_cannon": self.select_turret_cannon,
                "select_turret_core_debugger": self.select_turret_core_debugger
            }
        )

        # game logic에 영향을 받아서, 따로 들고 있어야 하는 ui들
        self.variable_uis = {
            "hp": Label(),
            "money": Label(),
            "current_round": Label()
        }
        self.variable_uis["hp"].load_ui(path=UI_PATH_HP)
        self.variable_uis["money"].load_ui(path=UI_PATH_MONEY)
        self.variable_uis["current_round"].load_ui(path=UI_PATH_ROUND)
        
        self.selected_turret_info_uis = None # 현재 그릴 정보창

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            # ui 이벤트 처리
            self.uis.handle_events(event)

    def update(self, dt):
        if self.wave_active:
            self.enemy_manager.update(dt)

            if self.enemy_manager.is_wave_done():
                self.wave_active = False
                print("웨이브 종료") # 확인용

        # 텍스트 ui 업데이트
        for key in self.variable_uis.keys():
            self.variable_uis[key].set_text(str(self.info[key]))

    def draw(self, screen):
        self.world.draw(screen)

        if self.wave_active:
            self.enemy_manager.draw(screen)

        # ui 그리기
        self.uis.draw(screen)
        # 정보창
        if self.selected_turret_info_uis:
            self.selected_turret_info_uis.draw(screen)
        # 골드, 라운드, 점수 등
        for ui in self.variable_uis.values():
            ui.draw(screen)