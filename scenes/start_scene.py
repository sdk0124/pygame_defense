# 게임 시작 씬

import pygame
from scenes.scene import Scene

from ui.image_button import ImageButton
from ui.ui_manager import UIManager
from ui.label import Label
from core.settings import UI_PATH_START_SCENE

class StartScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.uis = self.prepare_uis()

    # 씬 전환
    def game_start(self):
        from scenes.game_scene import GameScene
        self.switch_to(GameScene(self.game))

    # ui manager 생성
    def prepare_uis(self) -> UIManager:
        uis = UIManager()
        uis.load_uis(UI_PATH_START_SCENE, {"game_start": self.game_start})

        return uis

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            # ui event 처리
            self.uis.handle_events(event)
        
    def update(self, dt) -> None:
        pass

    def draw(self, screen):
        screen.fill((20, 20, 20))
        self.uis.draw(screen)