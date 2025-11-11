# (임시 버튼 클래스 -> 씬 전환 확인용)

import pygame

class Button:
    def __init__(self, x, y, width, height, text, font_size=32,
                 text_color=(255, 255, 255), color_idle=(70, 70, 70), color_hover=(100, 100, 100)):
        """
        간단한 텍스트 버튼 클래스
        :param x, y: 버튼 좌표 (왼쪽 상단)
        :param width, height: 버튼 크기
        :param text: 버튼에 표시할 문자열
        :param font_size: 폰트 크기
        :param text_color: 텍스트 색상
        :param color_idle: 평상시 버튼 색
        :param color_hover: 마우스 올릴 때 색
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.color_idle = color_idle
        self.color_hover = color_hover

        self.font = pygame.font.Font(None, font_size)
        self.hovered = False

    def handle_event(self, event):
        """이벤트 처리. 클릭 시 True 반환"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True

        return False

    def draw(self, surface):
        """버튼 렌더링"""
        color = self.color_hover if self.hovered else self.color_idle
        pygame.draw.rect(surface, color, self.rect, border_radius=8)

        # 텍스트 중앙 정렬
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
