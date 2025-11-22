import pygame

class World:
    def __init__(self, map_data, map_image):
        self.map_data = map_data
        self.map_image = map_image
        self.waypoints = []
        self.tile_map_data = None

    def process_data(self):
        """맵 데이터에서 원하는 정보 추출"""
        for layer in self.map_data["layers"]:
            if layer["name"] == "waypoints":
                self.process_waypoints(layer["objects"])
            if layer["name"] == "round_map":
                self.set_tile_map_data(layer["data"])

    def set_tile_map_data(self, tile_map_data):
        self.tile_map_data = tile_map_data

    def get_map_data(self):
        """타일 맵 데이터 반환"""
        return self.tile_map_data

    def process_waypoints(self, object_data):
        """적들이 이동하는 좌표 리스트 추출"""
        for obj in object_data:
            x = obj['x']
            y = obj['y']
            self.waypoints.append((x, y))

    def get_waypoints(self):
        return self.waypoints

    def draw(self, surface):
        surface.blit(self.map_image, (0, 0))

### 테스트 코드 ###
if __name__ == "__main__":

    from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    from entities.enemyManager import EnemyManager
    from resource_loader import load_map_data, load_map_image, load_enemy_images
    from data.enemy_data import ENEMY_DATA
    from data.wave_data import WAVE_DATA

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    world = World(load_map_data(), load_map_image())
    world.process_data()

    # print(world.get_waypoints())
    
    round_level = 2
    enemy_manager = EnemyManager(world.get_waypoints(), ENEMY_DATA, load_enemy_images())
    enemy_manager.set_wave(round_level - 1, WAVE_DATA)

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.draw(screen)
        enemy_manager.update(FPS)
        enemy_manager.draw(screen)
        pygame.display.flip()

    pygame.quit()