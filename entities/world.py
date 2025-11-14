import pygame

class World:
    def __init__(self, map_data, map_image):
        self.map_data = map_data
        self.map_image = map_image
        self.waypoints = []

    def process_data(self):
        """맵 데이터에서 원하는 정보 추출"""
        for layer in self.map_data["layers"]:
            if layer["name"] == "waypoints":
                self.process_waypoints(layer["objects"])                

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