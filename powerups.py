# powerups.py
import pygame
import random
from settings import *

class PowerUp:
    def __init__(self, type, x, y):
        self.type = type  # "score", "speed", "shield", "oil"
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = self._get_color()

    def _get_color(self):
        return {
            "score": (255, 215, 0),    # Золотой
            "speed": (255, 0, 0),      # Красный
            "shield": (0, 0, 255),     # Синий
            "oil": (0, 255, 0)         # Зеленый
        }[self.type]

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            self.color,
            (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y, 40, 40)
        )