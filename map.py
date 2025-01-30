# map.py
import pygame
import random
from settings import *
from powerups import PowerUp

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class GameMap:
    def __init__(self):
        self.image = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.image.fill(BACKGROUND_COLOR)
        self.objects = []
        self.powerups = []
        self.generate_objects()
        self.generate_powerups()

    def generate_objects(self):
        # Дорожная разметка
        for y in range(-100, MAP_HEIGHT + 100, 200):
            pygame.draw.line(
                self.image, 
                (255, 255, 255),
                (MAP_WIDTH // 2 - 50, y),
                (MAP_WIDTH // 2 + 50, y),
                10
            )
        # Кусты
        for _ in range(50):
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            pygame.draw.circle(self.image, (34, 139, 34), (x, y), 30)


 def generate_score_powerups(self):
        """Генерация обычных паверапов 'score'."""
        for _ in range(10):  # Обычные столбы с очками
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp("score", x, y))

    def generate_speed_powerups(self):
        """Генерация паверапов 'speed'."""
        for _ in range(3):  # Генерируем 3 паверапа скорости
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp("speed", x, y))

    def generate_shield_powerups(self):
        """Генерация паверапов 'shield'."""
        for _ in range(2):  # Генерируем 2 паверапа щита
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp("shield", x, y))

    def generate_oil_powerups(self):
        """Генерация паверапов 'oil'."""
        for _ in range(2):  # Генерируем 2 паверапа масла
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp("oil", x, y))

    def generate_special_powerups(self):
        """Генерация всех особых паверапов."""
        self.generate_speed_powerups()
        self.generate_shield_powerups()
        self.generate_oil_powerups()

    def check_collision(self, player_hitbox):
        for obj in self.objects:
            if player_hitbox.colliderect(obj.rect):
                return True
        return False

    def check_powerup_collision(self, player_hitbox):
        for p in self.powerups[:]:
            if player_hitbox.colliderect(p.rect):
                self.powerups.remove(p)
                return p.type
        return None

    def draw(self, screen, camera):
        screen.blit(self.image, (-camera.offset_x, -camera.offset_y))
        for p in self.powerups:
            p.draw(screen, camera)