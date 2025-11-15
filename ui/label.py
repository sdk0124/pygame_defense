# ui/label.py
import pygame, json
from ui.base import UIObject
from core.settings import FONT_PATH

class Label(UIObject):
    def __init__(self, x=0, y=0, w=0, text="", font_size=0, color=(255,255,255), layer=0):
        super().__init__(x, y, w, 0, layer)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(FONT_PATH, font_size)
        self.lines = self.wrap_text(text)

    def set_text(self, text_to_change):
        self.text = self.wrap_text(text_to_change)

    def wrap_text(self, text):
        """width에 맞게 자동 줄바꿈"""
        words = text.split(" ")
        lines = []
        cur = ""

        for word in words:
            test_line = cur + word + " "
            if self.rect.width == 0 or self.font.size(test_line)[0] <= self.rect.width:
                cur = test_line
            else:
                lines.append(cur)
                cur = word + " "
        lines.append(cur)
        return lines

    def draw(self, surface):
        if not self.visible:
            return

        y_offset = 0
        for line in self.lines:
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
            self.lines = self.wrap_text(self.text)

        if "font_size" in obj:
            self.font_size = obj["font_size"]
            self.font = pygame.font.Font(FONT_PATH, self.font_size)
            self.lines = self.wrap_text(self.text)

        if "color" in obj:
            self.color = tuple(obj["color"])

        # wrap 다시 적용
        self.lines = self.wrap_text(self.text)
