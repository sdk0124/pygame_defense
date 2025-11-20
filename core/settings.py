ROWS = 15               # 맵 타일 가로 칸 개수
COLS = 15               # 맵 타일 세로 칸 개수
CELL_SIZE = 64          # 한 타일의 가로, 세로 크기 (정사각형)
SIDE_WIDTH = 300        # 사이드 메뉴창 크기

SCREEN_WIDTH = (ROWS * CELL_SIZE) + SIDE_WIDTH      # 화면 가로
SCREEN_HEIGHT = (COLS * CELL_SIZE)                  # 화면 세로

TURRET_ANIM_STEPS = 6

FPS = 30

FONT_PATH = "assets/fonts/NanumGothic-Bold.ttf"
INFO_UI_PATH_CANNON = "ui/cannon_info_ui_layout.json"
INFO_UI_PATH_CORE_DEBUGGER = "ui/core_debugger_info_ui_layout.json"
UI_PATH_START_SCENE = "ui/start_scene_ui_layout.json"
UI_PATH_GAME_SCENE = "ui/game_scene_ui_layout.json"
UI_PATH_END_SCENE = "ui/end_scene_ui_layout.json"
UI_PATH_SCORE = "ui/score_ui_layout.json"
UI_PATH_MONEY = "ui/money_ui_layout.json"
UI_PATH_ROUND = "ui/round_ui_layout.json"