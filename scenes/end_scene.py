import pygame
from scenes.scene import Scene
from ui.ui_manager import UIManager
from ui.image_button import ImageButton
from ui.label import Label
from core.settings import UI_PATH_END_SCENE

class GameOverScene(Scene):
    def __init__(self, game, final_score: int = 0):
        super().__init__(game)
        self.final_score = final_score

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
        # text = Label(220, 200, 0, "GAME OVER", 80, (255, 80, 80))
        # score_surf = Label(320, 300, 0, f"SCORE: {self.final_score}", 36)
        # retry_button = ImageButton(300, 400, 200, 60, None, "RETRY", action=self.game_start)
        # exit_button = ImageButton(300, 480, 200, 60, None, "EXIT", action=self.go_to_start_scene)

        uis = UIManager()
        uis.load_uis(UI_PATH_END_SCENE, {"game_start": self.game_start, "go_to_start_scene": self.go_to_start_scene})

        return uis

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            self.uis.handle_events(event)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        self.uis.draw(screen)
