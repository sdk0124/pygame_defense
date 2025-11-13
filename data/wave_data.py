"""각 라운드 별로 스폰될 적 유형 및 개수"""
"""WAVE_DATA의 인덱스 값 + 1 : 해당 라운드"""
"""spawn_delay 단위 : ms (밀리초)"""

WAVE_DATA = [
    {
        "enemies" : {"byter" : 5},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 10},
        "spawn_delay" : 1000
    },
    {
        "enemies" : {"byter" : 5, "worm" : 5},
        "spawn_delay" : 1000
    }
]