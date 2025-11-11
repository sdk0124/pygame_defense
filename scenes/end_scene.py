import pygame
from scenes.scene import Scene
from ui.sample_button import Button

class GameOverScene(Scene):
    def __init__(self, game, final_score: int = 0):
        super().__init__(game)
        self.font = pygame.font.Font(None, 80)
        self.font_small = pygame.font.Font(None, 36)
        self.text = self.font.render("GAME OVER", True, (255, 80, 80))
        self.score_surf = self.font_small.render(f"SCORE: {final_score}", True, (255, 255, 255))
        self.retry_button = Button(300, 400, 200, 60, "RETRY")
        self.exit_button = Button(300, 480, 200, 60, "EXIT")

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                self.game.running = False

            if self.retry_button.handle_event(event):
                """게임 화면으로 이동"""
                from scenes.game_scene import GameScene
                self.switch_to(GameScene(self.game))

            if self.exit_button.handle_event(event):
                """(임시) 게임 시작 화면으로 이동"""
                from scenes.start_scene import StartScene
                self.switch_to(StartScene(self.game))

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        screen.blit(self.text, (220, 200))
        screen.blit(self.score_surf, (320, 300))
        self.retry_button.draw(screen)
        self.exit_button.draw(screen)
