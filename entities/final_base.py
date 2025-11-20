import pygame

class FinalBase(pygame.sprite.Sprite):
    def __init__(self, position, max_hp, image):
        super().__init__()
        self.position = position
        self.max_hp = max_hp
        self.hp = max_hp
        self.is_dead = False

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def get_isFinalBase_dead(self):
        return self.is_dead

    def take_damage(self):
        """최종 방어선 HP 감소"""
        self.hp -= 1

        if self.hp <= 0:
            self.is_dead = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)