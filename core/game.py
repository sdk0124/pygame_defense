import pygame
from scenes.scene_state_manager import SceneStateManager
from scenes.start_scene import StartScene
from core.settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption("CPU Defence")

        self.scene_manager = SceneStateManager(self)
        self.scene_manager.change_scene(StartScene(self))

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            state = self.scene_manager.get_scene()
            state.handle_events()
            state.update(dt)
            state.draw(self.screen)
            pygame.display.flip()