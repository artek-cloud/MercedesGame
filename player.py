# player.py
import pygame
import os
import math
from settings import *
import time

class Player:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, "resources", "car.png")
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
        except FileNotFoundError:
            print("Ошибка: файл car.png не найден!")
            original_image = pygame.Surface((50, 30))

        self.scale_factor = 0.2
        self.base_image = pygame.transform.scale(
            original_image,
            (int(original_image.get_width() * self.scale_factor),
             int(original_image.get_height() * self.scale_factor))
        )
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(MAP_WIDTH // 2, MAP_HEIGHT // 2))
        self.angle = 0
        self.speed = 0
        self.acceleration = 0.15
        self.max_speed = 8
        self.friction = 0.88
        self.hitbox = self.rect.inflate(-30, -30)
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.shield_active = False
        self.shield_timer = 0

    def update(self, keys):
        current_time = time.time()
        if self.speed_boost_active and current_time > self.speed_boost_timer:
            self.reset_max_speed()
            self.speed_boost_active = False
        if self.shield_active and current_time > self.shield_timer:
            self.shield_active = False

        if keys[pygame.K_LEFT]:
            self.angle += 4
        if keys[pygame.K_RIGHT]:
            self.angle -= 4
        self.angle %= 360

        if keys[pygame.K_UP]:
            self.speed += self.acceleration
        elif keys[pygame.K_DOWN]:
            self.speed -= self.acceleration * 0.5
        else:
            self.speed *= self.friction

        self.speed = max(-self.max_speed / 2, min(self.speed, self.max_speed))

        radians = math.radians(self.angle)
        dx = self.speed * math.cos(radians)
        dy = -self.speed * math.sin(radians)
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, MAP_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, MAP_HEIGHT - self.rect.height))
        self.hitbox.center = self.rect.center
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def increase_max_speed(self, factor, duration):
        self.max_speed *= factor
        self.speed_boost_active = True
        self.speed_boost_timer = time.time() + duration

    def reset_max_speed(self):
        self.max_speed = 8

    def activate_shield(self, duration):
        self.shield_active = True
        self.shield_timer = time.time() + duration

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))