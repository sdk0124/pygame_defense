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
from core.settings import INFO_UI_PATH_CORE_DEBUGGER, INFO_UI_PATH_CANNON, UI_PATH_GAME_SCENE, \
                        UI_PATH_HP, UI_PATH_MONEY, UI_PATH_ROUND, \
                        UI_PATH_SELECTED_CANNON, UI_PATH_SELECTED_CORE_DEBUGGER
from scenes.scene import Scene

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.wave_active = False
        self.wave_data = WAVE_DATA

        self.world = World(load_map_data(), load_map_image())
        self.world.process_data()

        self.enemy_manager = self.create_enemy_manager(self.handle_enemy_death)
        self.turret_manager = self.create_turret_manager(self.world.get_map_data())
        
        self.final_base = self.create_final_base(FINAL_BASE_POS, FINAL_BASE_DATA["max_hp"])

        self.info = {
            "money": 1000,
            "hp": self.final_base.get_FinalBase_curHp(),
            "score": 0,
            "current_round": 1
        }

        # 터렛 구매 모드인지 아닌 지
        self.is_turretPurchaseMode = False

        # ui 준비
        self.prepare_uis()

    def create_enemy_manager(self, handle_enemy_death):
        """enemyManager 생성"""
        enemy_images = load_enemy_images()
        waypoints = self.world.get_waypoints()
        return EnemyManager(waypoints, ENEMY_DATA, enemy_images, handle_enemy_death)

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
                                          COLS, turret_type, self.info["money"])

    def handle_enemy_death(self, enemy):
        """적 사망 시 골드/스코어 처리"""
        self.info["money"] += enemy.money
        self.info["score"] += enemy.score
        print(f"획득한 골드 : {enemy.money}, 획득 점수 : {enemy.score}")
        print(f"총 골드 : {self.info["money"]}, 총 점수 : {self.info["score"]}")

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
        self.switch_to(GameOverScene(self.game, self.info["score"]))
    
    # 터렛 선택 (캐논 터렛 구매 모드)
    def select_turret_cannon(self):
        self.selected_turret_info_uis = self.cannon_info_uis
        if self.selected_turret_uis != self.selected_turret_uis_cannon:
            self.selected_turret_uis = None
            self.selected_turret_type = None
        if self.turret_manager.get_isTurret_purchasable("cannon", self.info["money"]):
            print("c")
            self.selected_turret_uis = self.selected_turret_uis_cannon
            self.selected_turret_type = "cannon"
            self.is_turretPurchaseMode = True

    # 터렛 선택 (디버거 터렛 구매 모드)
    def select_turret_core_debugger(self):
        self.selected_turret_info_uis = self.core_debugger_info_uis
        if self.selected_turret_uis != self.selected_turret_uis_debugger:
            self.selected_turret_uis = None
            self.selected_turret_type = None
        if self.turret_manager.get_isTurret_purchasable("debugger", self.info["money"]):
            print("d")
            self.selected_turret_uis = self.selected_turret_uis_debugger
            self.selected_turret_type = "debugger"
            self.is_turretPurchaseMode = True

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
        self.selected_turret_uis = None # 현재 그릴 터렛

        self.selected_turret_type = None
        self.selected_turret_uis_cannon = UIManager(True)
        self.selected_turret_uis_cannon.load_uis(UI_PATH_SELECTED_CANNON)

        self.selected_turret_uis_debugger = UIManager(True)
        self.selected_turret_uis_debugger.load_uis(UI_PATH_SELECTED_CORE_DEBUGGER)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # 터렛 구매 모드일 경우
                if self.is_turretPurchaseMode:
                    # 터렛 구매
                    turretPlacedInfo = self.try_place_turret(mouse_pos, self.selected_turret_type)
                    if turretPlacedInfo:
                        self.info["money"] -= turretPlacedInfo['price']
                        
                    # 돈 부족하면 현재 선택된 터렛 이미지 없애기
                    if not self.turret_manager.get_isTurret_purchasable(self.selected_turret_type, self.info["money"]):
                        self.selected_turret_uis = None
                        self.selected_turret_type = None
                        self.is_turretPurchaseMode = False
                
                # 터렛 구매 모드가 아닐 경우
                else:
                    clicked_turret = self.turret_manager.get_turret_at_position(mouse_pos)

                    if (clicked_turret == None) or (clicked_turret.get_isSelected()):
                        self.turret_manager.clear_selection()
                    else:
                        self.turret_manager.set_selected_turret(clicked_turret)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

                # 현재 터렛 구매 모드에서 마우스 우클릭 시 터렛 구매 모드 해제
                if self.is_turretPurchaseMode:
                    self.selected_turret_uis = None
                    self.selected_turret_type = None
                    self.is_turretPurchaseMode = False

            # ui 이벤트 처리
            self.uis.handle_events(event)

    def update(self, dt):
        if self.wave_active:
            self.enemy_manager.update(dt, self.final_base)

            self.info["hp"] = self.final_base.get_FinalBase_curHp()

            if self.enemy_manager.is_wave_done():
                if self.info["current_round"] == 10:
                    self.go_to_game_end()
                self.info["current_round"] += 1
                self.wave_active = False
                print("웨이브 종료") # 확인용

            if self.final_base.get_isFinalBase_dead():
                self.go_to_game_end()
        
        self.turret_manager.update(dt, self.enemy_manager.enemies)

        # 텍스트 ui 업데이트
        for key in self.variable_uis.keys():
            self.variable_uis[key].set_text(str(self.info[key]))

        # 선택된 터렛 마우스 따라다님
        if self.selected_turret_uis:
            self.selected_turret_uis.update(dt)

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

        if self.is_turretPurchaseMode:
            self.selected_turret_uis.draw(screen)