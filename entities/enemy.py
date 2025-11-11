import pygame
from pygame.math import Vector2
from data.enemy_data import ENEMY_DATA

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, image):
        self.type = enemy_type
        self.waypoints = waypoints
        self.target_waypoint_idx = 1
        self.position = Vector2(self.waypoints[0])

        data = ENEMY_DATA[enemy_type]
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
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.position
        else:
            self.kill()

        dist = self.movement.length()

        if dist >= self.speed:
            self.position += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.position += self.movement.normalize() * dist
            self.target_waypoint += 1

    def draw(self, surface):
        """적 스프라이트 그리기"""
        surface.blit(self.image, self.rect)

    def update(self):
        "적 상태 갱신"
        self.move()

    