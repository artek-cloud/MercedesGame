# main.py
import pygame
import time
import traceback
import random
from settings import *
from camera import Camera
from map import GameMap
from player import Player
from audio import AudioManager
from ui import *
from crash_report import log_crash
from powerups import *

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Car Game")
        clock = pygame.time.Clock()

        # Инициализация
        camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        game_map = GameMap()
        player = Player()
        audio = AudioManager()
        audio.play_music()

        # Главное меню
        menu = MainMenu(screen, audio)
        in_menu = True
        while in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        in_menu = False
                menu.handle_event(event)
            menu.draw()

        # Ввод имени игрока
        player_name = input_name(screen)
        print(f"Игрок: {player_name}")
        
        SelectCharacter(screen)

        #running = True
        #while running:
        #    for event in pygame.event.get():
        #        if event.type == pygame.QUIT:
        #            running = False

        # Параметры игры
        POWERUP_SPAWN_INTERVAL = 10
        MAX_POWERUPS = {"score": 15, "speed": 5, "shield": 2, "oil": 2}
        last_powerup_spawn_time = time.time()
        player_score = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Управление машиной
            keys = pygame.key.get_pressed()
            player.update(keys)
            camera.update(player.rect)

            # Столкновение с препятствиями
            if game_map.check_collision(player.hitbox):
                if not player.shield_active:
                    print("Столкновение!")
                    player.speed *= -5
                    audio.play_sound("shield")

            # Взаимодействие с бонусами
            powerup_type = game_map.check_powerup_collision(player.hitbox)
            if powerup_type:
                audio.play_sound(powerup_type)
                if powerup_type == "speed":
                    player.increase_max_speed(1.5, 7)
                elif powerup_type == "score":
                    player_score += 100
                    player.increase_max_speed(1.05, 7)
                elif powerup_type == "shield":
                    player.activate_shield(10)
                elif powerup_type == "oil":
                    game_map.spawn_oil_spill()

            # Генерация бонусов
            current_time = time.time()
            if current_time - last_powerup_spawn_time > POWERUP_SPAWN_INTERVAL:
                powerup_counts = {"score": 0, "speed": 0, "shield": 0, "oil": 0}
                for p in game_map.powerups:
                    powerup_counts[p.type] += 1

                for powerup_type, max_count in MAX_POWERUPS.items():
                    if powerup_counts[powerup_type] < max_count:
                        x = random.randint(0, MAP_WIDTH)
                        y = random.randint(0, MAP_HEIGHT)
                        game_map.powerups.append(PowerUp(powerup_type, x, y))
                        break

                last_powerup_spawn_time = current_time

            # Отрисовка
            screen.fill(BACKGROUND_COLOR)
            game_map.draw(screen, camera)
            player.draw(screen, camera)
            draw_speed(screen, player.speed)
            draw_score(screen, player_score)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
    except Exception as e:
        error_message = traceback.format_exc()
        log_crash(error_message)
        print("Ошибка! Подробности в crash_report.txt.")
        pygame.quit()

if __name__ == "__main__":
    main()