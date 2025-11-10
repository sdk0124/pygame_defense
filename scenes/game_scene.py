# scenes/game_scene.py
import pygame
from ui.sample_button import Button
from scenes.scene import Scene

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # 임시 버튼
        self.end_button = Button(300, 400, 200, 60, "switch to Game Over")

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                self.game.running = False

            if self.end_button.handle_event(event):
                
                from scenes.end_scene import GameOverScene
                self.switch_to(GameOverScene(self.game, final_score=0))

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((50, 50, 80))
        self.end_button.draw(screen)
