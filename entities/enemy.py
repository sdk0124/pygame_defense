import pygame
from pygame.math import Vector2
from data.enemy_data import ENEMY_DATA

#### 임시 함수 시작 #####
points = []

def process_data(map_data):
    # look through data to extract info
    for layer in map_data["layers"]:
        if layer["name"] == "waypoints":
            for obj in layer["objects"]:
                process_waypoints(obj)

def process_waypoints(data):
    # iterate through waypoints to extract x, y
    x = data['x']
    y = data['y']
    points.append((x, y))

#### 임시 함수 끝 #####

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


### 테스트 코드 ###
if __name__ == "__main__":

    from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    from resource_loader import load_enemy_images, load_map_data, load_map_image

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    map_image = load_map_image()
    map_data = load_map_data()
    enemy_images = load_enemy_images()
    process_data(map_data)

    print(points)

    # enemy_images["byter"] = pygame.transform.scale(enemy_images["byter"], (64, 64))
    # enemy_images["worm"] = pygame.transform.scale(enemy_images["worm"], (64, 64))
    # enemy_images["boss"] = pygame.transform.scale(enemy_images["boss"], (128, 128))

    new_enemy = Enemy("byter", points, enemy_images["byter"])
    # new_enemy = Enemy("worm", points, enemy_images["worm"])
    # new_enemy = Enemy("boss", points, enemy_images["boss"])

    running = True

    # 임시로 스피드 조정
    new_enemy.speed = 5

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.blit(map_image, (0, 0))
        new_enemy.update()
        new_enemy.draw(screen)
        pygame.display.flip()
    
    pygame.quit()