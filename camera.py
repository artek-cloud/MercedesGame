# camera.py
from settings import MAP_WIDTH, MAP_HEIGHT

class Camera:
    def __init__(self, screen_width, screen_height):
        self.offset_x = 0
        self.offset_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, target_rect):
        self.offset_x = target_rect.centerx - self.screen_width // 2
        self.offset_y = target_rect.centery - self.screen_height // 2
        self.offset_x = max(0, min(self.offset_x, MAP_WIDTH - self.screen_width))
        self.offset_y = max(0, min(self.offset_y, MAP_HEIGHT - self.screen_height))