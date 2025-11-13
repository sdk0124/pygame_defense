import pygame
from pygame.math import Vector2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data, waypoints, image):
        super().__init__()
        self.waypoints = waypoints
        self.target_waypoint_idx = 1
        self.position = Vector2(self.waypoints[0])

        data = enemy_data
        self.max_hp = data["max_hp"]
        self.hp = self.max_hp
        self.speed = data["speed"]
        self.money = data["money"]
        self.score = data["score"]

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def move(self):
        """waypoint에 맞춰서 적이 이동"""
        if self.target_waypoint_idx < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint_idx])
            self.movement = self.target - self.position
        else:
            pass
            # 다 도달했으면 해당 적은 삭제되고 최종 방어 타워의 체력 1만큼 감소.
            # self.kill()

        dist = self.movement.length()

        if dist >= self.speed:
            self.position += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.position += self.movement.normalize() * dist
            self.target_waypoint_idx += 1
        
        self.rect.center = self.position

    def drew_health_bar(self, surface):
        """적 HP 바 그리기"""
        ratio = max(self.hp / self.max_hp, 0)

        bar_width = self.rect.width
        bar_height = 10
        bar_x = self.rect.x
        bar_y = self.rect.y - 10

        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * ratio, bar_height))

    def draw(self, surface):
        """적 스프라이트 그리기"""
        surface.blit(self.image, self.rect)
        self.drew_health_bar(surface)

    def update(self):
        "적 상태 갱신"
        self.move()