import pygame
from entities.turret import Turret
from core.settings import CELL_SIZE

class TurretManager:
    def __init__(self, world_tilemap, turret_data_table, turret_image_table):
        self.world_tilemap = world_tilemap
        self.turret_data_table = turret_data_table
        self.turret_image_table = turret_image_table
        self.turrets = pygame.sprite.Group()
        self.selected_turret = None

    def create_turret(self, mouse_pos, max_width, max_height, tile_size, col, turret_type, money):
        if (mouse_pos[0] > max_width) or (mouse_pos[1] > max_height):
            print("해당 위치에 터렛을 설치할 수 없습니다.")
            return None

        """해당 타일에 터렛 설치 시도"""
        grid_x = mouse_pos[0] // tile_size
        grid_y = mouse_pos[1] // tile_size

        mouse_tile_num = (grid_y * col) + grid_x

        # 41 : 타일맵에서 터렛 설치가 가능한 공간을 의미.
        if self.world_tilemap[mouse_tile_num] != 41:
            print("터렛을 설치할 수 없는 구역입니다.")
            return None

        for turret in self.turrets:
            # 이미 설치된 곳은 설치하면 안됨.
            if (grid_x, grid_y) == (turret.tile_x, turret.tile_y):
                print("이미 터렛이 설치된 구역입니다.")
                return None
        
        turret_data = self.turret_data_table[turret_type]
        price = turret_data["purchase_price"]
        if (money < price):
            print("해당 터렛을 구매할 수 없습니다.")
            return None

        turret_idle_image = self.turret_image_table[turret_type]["idle"]
        turret_attack_images = self.turret_image_table[turret_type]["attack"]
        
        new_turret = Turret(grid_x, grid_y,
                            tile_size,
                            turret_data,
                            turret_idle_image,
                            turret_attack_images)
        
        self.turrets.add(new_turret)

        print(f"터렛이 설치됨: ({grid_x}, {grid_y})") # 테스트용
        return {'isTurretPlaced' : True, 'price' : price}

    def get_turret_at_position(self, mouse_pos):
        """현재 좌표에 존재하는 터렛 반환, 없으면 None"""
        for turret in self.turrets:
            if turret.rect.collidepoint(mouse_pos):
                return turret
        return None

    def set_selected_turret(self, turret):
        """터렛 선택 상태 결정"""
        self.selected_turret = turret
        for existing_turret in self.turrets:
            existing_turret.is_selected = (existing_turret is turret)

    def clear_selection(self):
        """선택된 터렛 해제"""
        self.selected_turret = None
        for turret in self.turrets:
            turret.is_selected = False

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

    player_money = 2000

    running = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                turretPlacedInfo = turret_manager.create_turret(mouse_pos, map_width, map_height, CELL_SIZE, COLS, "debugger", player_money)
                if turretPlacedInfo:
                    player_money -= turretPlacedInfo['price']

        world.draw(screen)

        enemy_manager.update(dt)
        turret_manager.update(dt, enemy_manager.enemies)

        enemy_manager.draw(screen)
        turret_manager.draw(screen)

        pygame.display.flip()
    
    pygame.quit()