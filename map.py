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


    def generate_powerups(self):
        types = ["score", "speed", "shield", "oil"]
        for _ in range(10):  # Обычные столбы с очками
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp("score", x, y))
        for t in ["speed", "shield", "oil"]:  # Особые паверапы
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp(t, x, y))

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