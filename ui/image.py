# ui/image.py
import pygame, os, json
from ui.base import UIObject

class UIImage(UIObject):
    def __init__(self, x=0, y=0, w=128, h=128, image_path="assets/default_button.png", layer=0):
        super().__init__(x, y, w, h, layer)
        self.image_path = image_path
        self.image = None
        self.load_image()

    def load_image(self):
        if os.path.exists(self.image_path):
            img = pygame.image.load(self.image_path).convert_alpha()
            self.image = pygame.transform.scale(img, (self.rect.width, self.rect.height))
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill((120, 120, 120))

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)

    def load_ui(self, obj=None, path=None):
        if path:
            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)["objects"][0]
        super().load_ui(obj)

        if "image" in obj:
            self.image_path = obj["image"]
            self.image = pygame.image.load(obj["image"]).convert_alpha()
            # rect 크기 업데이트
            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()