# ui/image_button.py
import pygame, os, json
from ui.base import UIObject
from core.settings import FONT_PATH

class ImageButton(UIObject):
    def __init__(self, x, y, width, height, image_path="", text="", font_size=32,
                 text_color=(255,255,255),
                 color_idle=(60,60,60),
                 action=None,
                 sound_path=None,
                 layer=0):
        
        super().__init__(x, y, width, height, layer)
        self.text = text
        self.font = pygame.font.Font(FONT_PATH, font_size)
        self.font_size = font_size
        self.text_color = text_color
        self.color_idle = color_idle
        self.hovered = False
        self.action = action
        self.sound_path = sound_path
        self.sound = None
        self.image_path = image_path if image_path else ""
        self.image = None

    def load_image(self):
        if self.image_path != "" and os.path.exists(self.image_path):
            img = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(img, (self.rect.width, self.rect.height))
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill((120, 120, 120))

    def load_sound(self):
        """사운드 파일 로드 (없으면 무시)"""
        if self.sound_path and os.path.exists(self.sound_path):
            try:
                self.sound = pygame.mixer.Sound(self.sound_path)
            except pygame.error as e:
                print(f"⚠️ 사운드 로드 실패: {self.sound_path} ({e})")
                self.sound = None
        else:
            self.sound = None

    def click(self):
        """버튼 클릭 시 사운드 & 액션"""
        if self.sound:
            self.sound.play()
        print(f"🔘 버튼 클릭됨: {self.text} | action={self.action}")

    def apply_hover_brightness(self, image, amount=40):
        img = image.copy()
        overlay = pygame.Surface(img.get_size()).convert()
        overlay.fill((amount, amount, amount))
        img.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        return img

    def handle_event(self, event) -> bool:
        if not self.visible:
            return False
        
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

        if self.image is not None:
            # hover 효과
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                img_to_draw = self.apply_hover_brightness(self.image)
            else:
                img_to_draw = self.image

            # 이미지 중앙배치
            img_rect = img_to_draw.get_rect(center=self.rect.center)
            surface.blit(img_to_draw, img_rect)

        # 텍스트
        lines = self.text.split("\n")
        y_offset = 0
        for line in lines:
            surf = self.font.render(line, True, self.text_color)
            text_rect = surf.get_rect(center=self.rect.center)
            surface.blit(surf, (text_rect.x, text_rect.y + y_offset))
            y_offset += surf.get_height()
        

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

        # 버튼 이미지
        if "image_path" in obj:
            self.image_path = obj["image_path"]
            self.load_image()

        if "sound_path" in obj:
            if obj["sound_path"]:
                self.load_sound()

        # action (Scene에서 넘겨줄 bind_action dict 필요)
        if "action" in obj:
            self.action_name = obj["action"]   # 임시 저장