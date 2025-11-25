# ui/label.py
import pygame, json
from ui.base import UIObject
from core.settings import FONT_PATH

class Label(UIObject):
    def __init__(self, x=0, y=0, width=0, text="", font_size=0, color=(255,255,255), layer=0):
        super().__init__(x, y, width, 0, layer)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(FONT_PATH, font_size)

    def set_text(self, text_to_change):
        self.text = text_to_change

    def draw(self, surface):
        if not self.visible:
            return

        lines = self.text.split("\n")
        y_offset = 0
        for line in lines:
            surf = self.font.render(line, True, self.color)
            surface.blit(surf, (self.rect.x, self.rect.y + y_offset))
            y_offset += surf.get_height()

    def load_ui(self, obj=None, path=None):
        if path:
            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)["objects"][0]
        super().load_ui(obj)

        if "text" in obj:
            self.text = obj["text"]

        if "font_size" in obj:
            self.font_size = obj["font_size"]
            self.font = pygame.font.Font(FONT_PATH, self.font_size)

        if "color" in obj:
            self.color = tuple(obj["color"])
