# 씬을 관리하는 클래스

class SceneStateManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = None

    def get_scene(self):
        return self.current_scene

    def change_scene(self, target_scene):
        self.current_scene = target_scene