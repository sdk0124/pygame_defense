# 씬 추상클래스

from __future__ import annotations
from abc import ABC, abstractmethod
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.game import Game

class Scene(ABC):
    """모든 씬의 공통 인터페이스를 강제하는 추상 클래스."""
    
    def __init__(self, game: "Game") -> None:
        self.game = game

    @abstractmethod
    def handle_events(self) -> None:
        """입력/이벤트 처리"""
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        """게임 로직 업데이트. dt는 초 단위(delta time)."""
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """렌더링"""
        raise NotImplementedError
    
    # 씬 전환 메소드
    def switch_to(self, next_scene: "Scene") -> None:
        self.game.scene_manager.change_scene(next_scene)
        print("Move to next Scene")