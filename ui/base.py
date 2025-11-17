# ui/base.py
import pygame

class UIObject:
    def __init__(self, x, y, w, h, layer):
        self.rect = pygame.Rect(x, y, w, h)
        self.visible = True
        self.alpha = 255
        self.layer = layer

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
        if "w" in obj: self.rect.width = obj["w"]
        if "h" in obj: self.rect.height = obj["h"]
        if "layer" in obj: self.layer = obj["layer"]
        if "visible" in obj: self.visible = obj["visible"]
        if "alpha" in obj:  self.alpha = obj["alpha"]
