# ui/image_button.py
import pygame, os, json
from ui.base import UIObject
from core.settings import FONT_PATH

class ImageButton(UIObject):
    def __init__(self, x, y, w, h, image_path, text, font_size=32,
                 text_color=(255,255,255),
                 color_idle=(60,60,60),
                 color_hover=(90,90,90),
                 action=None,
                 layer=0):
        
        super().__init__(x, y, w, h, layer)
        self.text = text
        self.font = pygame.font.Font(FONT_PATH, font_size)
        self.font_size = font_size
        self.text_color = text_color
        self.color_idle = color_idle
        self.color_hover = color_hover
        self.hovered = False
        self.action = action
        self.image_path = image_path if image_path else ""
        self.image = None
        self.load_image()

    def load_image(self):
        if os.path.exists(self.image_path):
            img = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(img, (self.rect.width, self.rect.height))
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill((120, 120, 120))

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()
                return True  # 클릭됨

        return False

    def draw(self, surface):
        if not self.visible:
            return

        # 배경
        color = self.color_hover if self.hovered else self.color_idle
        pygame.draw.rect(surface, color, self.rect, border_radius=8)

        # 이미지 중앙배치
        if self.image is not None:
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)

        # 텍스트
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def load_ui(self, obj=None, path=None):
        if path:
            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)["objects"][0]
        super().load_ui(obj)

        # 텍스트
        if "text" in obj:
            self.text = obj["text"]

        # 폰트
        if "font_size" in obj:
            self.font_size = obj["font_size"]
            self.font = pygame.font.Font(FONT_PATH, self.font_size)

        if "text_color" in obj:
            self.text_color = tuple(obj["text_color"])

        # 배경 색
        if "color_idle" in obj:
            self.color_idle = tuple(obj["color_idle"])

        if "color_hover" in obj:
            self.color_hover = tuple(obj["color_hover"])

        # 버튼 이미지
        if "image" in obj:
            self.image = pygame.image.load(obj["image"]).convert_alpha()

        # action (Scene에서 넘겨줄 bind_action dict 필요)
        if "action" in obj:
            self.action_name = obj["action"]   # 임시 저장