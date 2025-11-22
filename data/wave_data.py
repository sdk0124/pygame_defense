"""각 라운드 별로 스폰될 적 유형 및 개수"""
"""WAVE_DATA의 인덱스 값 + 1 : 해당 라운드"""
"""spawn_delay 단위 : ms (밀리초)"""

WAVE_DATA = [
    {
        "enemies" : {"byter" : 5},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 7},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 9, "worm" : 1},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 8, "worm" : 3},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 6, "worm" : 5},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 5, "worm" : 7},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 4, "worm" : 9},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 4, "worm" : 12},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 3, "worm" : 15},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"boss" : 1},
        "spawn_delay" : 1000
    },
]