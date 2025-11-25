import pygame
from scenes.scene import Scene
from ui.ui_manager import UIManager
from ui.image_button import ImageButton
from ui.label import Label
from core.settings import UI_PATH_END_SCENE, UI_PATH_SCORE

class GameOverScene(Scene):
    def __init__(self, game, final_score: int = 0):
        super().__init__(game)
        self.info = {
            "final_score": final_score
        }

        self.uis = self.prepare_uis()

    def game_start(self):
        """게임 화면으로 이동"""
        from scenes.game_scene import GameScene
        self.switch_to(GameScene(self.game))

    def go_to_start_scene(self):
        """(임시) 게임 시작 화면으로 이동"""
        from scenes.start_scene import StartScene
        self.switch_to(StartScene(self.game))

    def prepare_uis(self):
        uis = UIManager()
        uis.load_uis(UI_PATH_END_SCENE, {"game_start": self.game_start, "go_to_start_scene": self.go_to_start_scene})

        # game logic에 영향을 받아서, 따로 들고 있어야 하는 ui들
        self.variable_uis = {
            "final_score": Label()
        }
        self.variable_uis["final_score"].load_ui(path=UI_PATH_SCORE)

        return uis

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            self.uis.handle_events(event)

    def update(self, dt: float) -> None:
        # 텍스트 ui 업데이트
        for key in self.variable_uis.keys():
            self.variable_uis[key].set_text(str(self.info[key]))

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        self.uis.draw(screen)

        # 점수 등
        for ui in self.variable_uis.values():
            ui.draw(screen)
