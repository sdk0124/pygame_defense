from core.paths import resource_path

ROWS = 15               # 맵 타일 가로 칸 개수
COLS = 15               # 맵 타일 세로 칸 개수
CELL_SIZE = 64          # 한 타일의 가로, 세로 크기 (정사각형)
SIDE_WIDTH = 300        # 사이드 메뉴창 크기

SCREEN_WIDTH = (ROWS * CELL_SIZE) + SIDE_WIDTH      # 화면 가로
SCREEN_HEIGHT = (COLS * CELL_SIZE)                  # 화면 세로

TURRET_ANIM_STEPS = 6
FINAL_BASE_POS = (920, 830)
FPS = 30

START_MONEY = 300   # 시작 시 플레이어에게 주어진 초기 돈

FONT_PATH = resource_path("assets", "fonts", "NanumGothic-Bold.ttf")
INFO_UI_PATH_CANNON = resource_path("ui", "ui_layouts", "cannon_info_ui_layout.json")
INFO_UI_PATH_CORE_DEBUGGER = resource_path("ui", "ui_layouts", "core_debugger_info_ui_layout.json")
UI_PATH_START_SCENE = resource_path("ui", "ui_layouts", "start_scene_ui_layout.json")
UI_PATH_GAME_SCENE = resource_path("ui", "ui_layouts", "game_scene_ui_layout.json")
UI_PATH_END_SCENE = resource_path("ui", "ui_layouts", "end_scene_ui_layout.json")

UI_PATH_HP = resource_path("ui", "ui_layouts", "hp_ui_layout.json")
UI_PATH_MONEY = resource_path("ui", "ui_layouts", "money_ui_layout.json")
UI_PATH_ROUND = resource_path("ui", "ui_layouts", "round_ui_layout.json")

UI_PATH_SELECTED_CANNON = resource_path("ui", "ui_layouts", "cannon_selected_ui_layout.json")
UI_PATH_SELECTED_CORE_DEBUGGER = resource_path("ui", "ui_layouts", "core_debugger_selected_ui_layout.json")

UI_PATH_SCORE = resource_path("ui", "ui_layouts", "score_ui_layout.json")