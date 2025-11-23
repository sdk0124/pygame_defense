# ui/base.py
import pygame

class UIObject:
    def __init__(self, x, y, width, height, layer):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.alpha = 255
        self.layer = layer

    def move(self, to_x, to_y):
        self.rect.center = (to_x, to_y)

    def set_visible(self, flag: bool):
        self.visible = flag

    def draw(self, surface):
        pass

    def update(self, dt):
        pass

    def handle_event(self, event):
        pass

    def load_ui(self, obj):
        # 공통 속성 불러오기
        if "x" in obj: self.rect.x = obj["x"]
        if "y" in obj: self.rect.y = obj["y"]
        if "width" in obj: self.rect.width = obj["width"]
        if "height" in obj: self.rect.height = obj["height"]
        if "layer" in obj: self.layer = obj["layer"]
        # 추가할 거
        if "activated" in obj: self.visible = obj["activated"]
        if "alpha" in obj:  self.alpha = obj["alpha"]
