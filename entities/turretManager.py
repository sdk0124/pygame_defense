import pygame
from entities.turret import Turret
from core.settings import CELL_SIZE

class TurretManager:
    def __init__(self, world_tilemap, turret_data_table, turret_image_table):
        self.world_tilemap = world_tilemap
        self.turret_data_table = turret_data_table
        self.turret_image_table = turret_image_table
        self.turrets = pygame.sprite.Group()

    def create_turret(self, mouse_pos, max_width, max_height, tile_size, col, turret_type, money):
        if (mouse_pos[0] > max_width) or (mouse_pos[1] > max_height):
            print("해당 위치에 터렛을 설치할 수 없습니다.")
            return False, 0

        turret_data = self.turret_data_table[turret_type]
        price = turret_data[turret_type]["purchase_price"]
        if (money < price):
            print("해당 터렛을 구매할 수 없습니다.")
            return False, 0

        """해당 타일에 터렛 설치"""
        grid_x = mouse_pos[0] // tile_size
        grid_y = mouse_pos[1] // tile_size

        mouse_tile_num = (grid_y * col) + grid_x

        # 41 : 타일맵에서 길이 아닌 곳을 의미.
        if self.world_tilemap[mouse_tile_num] == 41:
            for turret in self.turrets:
                # 이미 설치된 곳은 설치하면 안됨.
                if (grid_x, grid_y) == (turret.tile_x, turret.tile_y):
                    return
                        
            turret_idle_image = self.turret_image_table[turret_type]["idle"]
            turret_attack_images = self.turret_image_table[turret_type]["attack"]
            
            new_turret = Turret(grid_x, grid_y,
                                tile_size,
                                turret_data,
                                turret_idle_image,
                                turret_attack_images)
            
            self.turrets.add(new_turret)

            print(f"터렛이 설치됨: ({grid_x}, {grid_y})") # 테스트용
            return True, price

    def update(self, dt, enemies):
        for turret in self.turrets:
            turret.update(dt, enemies)
    
    def draw(self, surface):
        for turret in self.turrets:
            turret.draw(surface)

### 테스트 코드 ###
if __name__ == "__main__":

    from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CELL_SIZE, ROWS, COLS
    from resource_loader import load_enemy_images, load_map_data, load_map_image, load_turret_images
    
    from entities.enemyManager import EnemyManager
    from entities.world import World

    from data.turret_data import TURRET_DATA
    from data.enemy_data import ENEMY_DATA
    from data.wave_data import WAVE_DATA

    ### 임시 함수 및 임시 상수 ###

    TURRET_ANIM_STEPS = 6

    def set_attack_images(attack_spritesheet):
        size = attack_spritesheet.get_height()
        attack_images = []

        for x in range(TURRET_ANIM_STEPS):
            temp_image = attack_spritesheet.subsurface(x * size, 0, size, size)
            attack_images.append(temp_image)

        return attack_images

    def set_tile_map(map_data):
        for layer in map_data["layers"]:
            if layer["name"] == "round_map":
                return layer["data"]

    ### 임시 함수 및 임시 상수 끝 ###


    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    world = World(load_map_data(), load_map_image())
    world.process_data()

    tilemap = set_tile_map(world.map_data) # 임시
    print(tilemap) # 임시

    enemy_images = load_enemy_images()
    turret_images = load_turret_images()

    cur_wave_round = 3
    wave_data = WAVE_DATA

    enemy_manager = EnemyManager(world.get_waypoints(), ENEMY_DATA, enemy_images)
    enemy_manager.set_wave(cur_wave_round - 1, wave_data)

    turret_manager = TurretManager(tilemap, TURRET_DATA, turret_images)

    map_width = ROWS * CELL_SIZE
    map_height = COLS * CELL_SIZE

    running = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                turret_manager.create_turret(mouse_pos, map_width, map_height, CELL_SIZE, COLS, "debugger")
            
        world.draw(screen)

        enemy_manager.update(dt)
        turret_manager.update(dt, enemy_manager.enemies)

        enemy_manager.draw(screen)
        turret_manager.draw(screen)

        pygame.display.flip()
    
    pygame.quit()