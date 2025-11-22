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

    def get_FinalBase_curHp(self):
        return self.hp

    def get_isFinalBase_dead(self):
        return self.is_dead

    def take_damage(self):
        """최종 방어선 HP 감소"""
        self.hp -= 1
        print(f"공격 받았습니다. 남은 hp : {self.hp}")

        if self.hp <= 0:
            self.is_dead = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

### 테스트 코드 ###
if __name__ == "__main__":

    from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CELL_SIZE, ROWS, COLS, FINAL_BASE_POS
    from resource_loader import load_enemy_images, load_map_data, load_map_image, load_turret_images, load_final_base_image
    
    from entities.enemyManager import EnemyManager
    from entities.world import World
    from entities.turretManager import TurretManager

    from data.turret_data import TURRET_DATA
    from data.enemy_data import ENEMY_DATA
    from data.wave_data import WAVE_DATA
    from data.final_base_data import FINAL_BASE_DATA

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
    final_base_image = load_final_base_image()

    cur_wave_round = 3
    wave_data = WAVE_DATA

    final_base = FinalBase(FINAL_BASE_POS, FINAL_BASE_DATA["max_hp"], final_base_image)

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

        if final_base.get_isFinalBase_dead():
            print("게임 오버 화면으로 이동")

        world.draw(screen)

        enemy_manager.update(dt, final_base)
        turret_manager.update(dt, enemy_manager.enemies)

        enemy_manager.draw(screen)
        turret_manager.draw(screen)

        final_base.draw(screen)

        pygame.display.flip()
    
    pygame.quit()