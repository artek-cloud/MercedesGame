# powerups.py
import pygame

class PowerUp:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = self._get_color()

    def _get_color(self):
        return {
            "score": (255, 215, 0),
            "speed": (255, 0, 0),
            "shield": (0, 0, 255),
            "oil": (0, 255, 0)
        }[self.type]

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            self.color,
            (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y, 40, 40)
        )