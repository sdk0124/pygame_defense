# scenes/game_scene.py
import pygame

from resource_loader import load_map_image, load_map_data, load_enemy_images, load_turret_images, load_final_base_image
from entities.world import World
from entities.enemyManager import EnemyManager
from entities.turretManager import TurretManager
from entities.final_base import FinalBase
from core.settings import FINAL_BASE_POS, ROWS, COLS, CELL_SIZE

from data.turret_data import TURRET_DATA
from data.enemy_data import ENEMY_DATA
from data.wave_data import WAVE_DATA
from data.final_base_data import FINAL_BASE_DATA

from ui.ui_manager import UIManager
from ui.image_button import ImageButton
from ui.label import Label
from core.settings import INFO_UI_PATH_CORE_DEBUGGER, INFO_UI_PATH_CANNON, UI_PATH_GAME_SCENE, UI_PATH_SCORE, UI_PATH_MONEY, UI_PATH_ROUND
from scenes.scene import Scene

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.score = 0
        self.money = 1000 # 임시
        self.current_round = 1
        self.wave_active = False
        self.wave_data = WAVE_DATA

        self.world = World(load_map_data(), load_map_image())
        self.world.process_data()

        self.enemy_manager = self.create_enemy_manager()
        self.turret_manager = self.create_turret_manager(self.world.get_map_data())
        
        self.final_base = self.create_final_base(FINAL_BASE_POS, FINAL_BASE_DATA["max_hp"])

        # ui 준비
        self.prepare_uis()

    def create_enemy_manager(self):
        """enemyManager 생성"""
        enemy_images = load_enemy_images()
        waypoints = self.world.get_waypoints()
        return EnemyManager(waypoints, ENEMY_DATA, enemy_images)

    def create_turret_manager(self, map_data):
        """TurretManager 생성"""
        turret_images = load_turret_images()
        return TurretManager(map_data, TURRET_DATA, turret_images)

    def create_final_base(self, position, max_hp):
        """Final Base 생성"""
        final_base_image = load_final_base_image()
        return FinalBase(position, max_hp, final_base_image)

    def try_place_turret(self, mouse_pos, turret_type):
        """터렛 설치 시도"""
        map_width = ROWS * CELL_SIZE
        map_height = COLS * CELL_SIZE
        return self.turret_manager.create_turret(mouse_pos, map_width,
                                          map_height, CELL_SIZE,
                                          COLS, turret_type, self.money)
        
    # 버튼 눌리면 호출할 함수
    def start_wave(self):
        """
        현재 웨이브가 비활성화 상태이고,
        그 때 유저가 '웨이브 시작' 버튼을 누르면 웨이브 생성
        """
        if not self.wave_active:
            self.enemy_manager.set_wave(self.current_round - 1, self.wave_data)
            self.wave_active = True

    # 버튼 눌리면 호출할 함수
    def go_to_game_end(self):
        """게임 오버 화면으로 이동"""
        from scenes.end_scene import GameOverScene
        self.switch_to(GameOverScene(self.game, final_score=0))

    # ui manager 생성
    def prepare_uis(self) -> UIManager:
        # round_start_button = ImageButton(800, 400, 200, 60, None, "Round Start!", action=self.start_wave)
        # end_button = ImageButton(600, 400, 200, 60, None, "switch to Game Over", action=self.go_to_game_end)
        self.cannon_info_uis = UIManager()
        self.cannon_info_uis.load_uis(INFO_UI_PATH_CANNON)
        self.core_debugger_info_uis = UIManager()
        self.core_debugger_info_uis.load_uis(INFO_UI_PATH_CORE_DEBUGGER)
        self.uis = UIManager()
        self.uis.load_uis(UI_PATH_GAME_SCENE, {"start_wave": self.start_wave, "go_to_game_end": self.go_to_game_end})

        # game logic에 영향을 받아서, 따로 들고 있어야 하는 ui들
        self.variable_uis = {
            "score": Label(),
            "money": Label(),
            "current_round": Label()
        }
        self.variable_uis["score"].load_ui(path=UI_PATH_SCORE)
        self.variable_uis["money"].load_ui(path=UI_PATH_MONEY)
        self.variable_uis["current_round"].load_ui(path=UI_PATH_ROUND)
        
        self.selected_turret_info_uis = None # 현재 그릴 정보창
        # self.uis.add(round_start_button)
        # self.uis.add(end_button)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            """ 임시 이벤트 """
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                turretPlacedInfo = self.try_place_turret(mouse_pos, "debugger")
                if turretPlacedInfo:
                    self.money -= turretPlacedInfo['price']
            """ 임시 이벤트 끝 """

            # ui 이벤트 처리
            self.uis.handle_events(event)

    def update(self, dt):
        if self.wave_active:
            self.enemy_manager.update(dt, self.final_base)

            if self.enemy_manager.is_wave_done():
                self.wave_active = False
                print("웨이브 종료") # 확인용
        
        self.turret_manager.update(dt, self.enemy_manager.enemies)

    def draw(self, screen):
        self.world.draw(screen)

        if self.wave_active:
            self.enemy_manager.draw(screen)

        self.turret_manager.draw(screen)
        self.final_base.draw(screen)

        # ui 그리기
        self.uis.draw(screen)
        # 정보창
        if self.selected_turret_info_uis:
            self.selected_turret_info_uis.draw(screen)
        # 골드, 라운드, 점수 등
        for ui in self.variable_uis.values():
            ui.draw(screen)