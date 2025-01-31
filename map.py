# map.py
import pygame
import random
from settings import *
from powerups import PowerUp

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (width//2, height//2), width//2)

class GameMap:
    def __init__(self):
        self.image = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.image.fill(BACKGROUND_COLOR)
        self.objects = pygame.sprite.Group()
        self.powerups = []
        self.generate_objects()
        self.generate_special_powerups()

    def generate_objects(self):
        # Дорожная разметка
        for y in range(-100, MAP_HEIGHT + 100, 200):
            pygame.draw.line(
                self.image, (255, 255, 255),
                (MAP_WIDTH//2 - 50, y), (MAP_WIDTH//2 + 50, y), 10
            )
        # Кусты
        for _ in range(50):
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            pygame.draw.circle(self.image, (34, 139, 34), (x, y), 30)
        # Препятствия
        for _ in range(10):
            obj = GameObject(random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT), 30, 30)
            self.objects.add(obj)

    def generate_score_powerups(self):
        for _ in range(10):
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp("score", x, y))

    def generate_speed_powerups(self):
        for _ in range(3):
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp("speed", x, y))

    def generate_shield_powerups(self):
        for _ in range(2):
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp("shield", x, y))

    def generate_oil_powerups(self):
        for _ in range(2):
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            self.powerups.append(PowerUp("oil", x, y))

    def generate_special_powerups(self):
        self.generate_speed_powerups()
        self.generate_shield_powerups()
        self.generate_oil_powerups()

    def spawn_oil_spill(self):
        x = random.randint(0, MAP_WIDTH)
        y = random.randint(0, MAP_HEIGHT)
        self.powerups.append(PowerUp("oil", x, y))

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
        for obj in self.objects:
            screen.blit(obj.image, (obj.rect.x - camera.offset_x, obj.rect.y - camera.offset_y))
        for p in self.powerups:
            p.draw(screen, camera)