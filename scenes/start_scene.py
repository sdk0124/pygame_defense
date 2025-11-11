# 게임 시작 씬

import pygame
from scenes.scene import Scene

from ui.sample_button import Button

class StartScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.font = pygame.font.Font(None, 80)
        self.title = self.font.render("CPU DEFENSE", True, (255, 255, 255))

        self.start_button = Button(300, 400, 200, 60, "START")

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                self.game.running = False

            if self.start_button.handle_event(event):

                from scenes.game_scene import GameScene
                self.switch_to(GameScene(self.game))
        
    def update(self, dt) -> None:
        pass

    def draw(self, screen):
        screen.fill((20, 20, 20))
        screen.blit(self.title, (220, 200))
        self.start_button.draw(screen)