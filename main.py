# main.py
import pygame
import time
import traceback  # Для получения трассировки стека
import random
from settings import *
from camera import Camera
from map import GameMap
from player import Player
from audio import AudioManager
from ui import MainMenu, input_name, draw_speed
from crash_report import log_crash  # Импортируем функцию для записи краш-репортов
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

        # Параметры для генерации паверапов
        POWERUP_SPAWN_INTERVAL = 10  # Интервал между попытками создания паверапов (в секундах)
        MAX_POWERUPS = {
            "score": 15,  # Максимальное количество паверапов "score"
            "speed": 5,  # Максимальное количество паверапов "speed"
            "shield": 2,  # Максимальное количество паверапов "shield"
            "oil": 2      # Максимальное количество паверапов "oil"
        }
        last_powerup_spawn_time = time.time()  # Время последней попытки создания паверапов

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Управление машиной
            keys = pygame.key.get_pressed()
            player.update(keys)
            camera.update(player.rect)

            # Проверка столкновений
            if game_map.check_collision(player.hitbox):
                print("Столкновение с препятствием!")
                player.speed *= -5  # Изменяем скорость на -5
                audio.play_sound("shield")  # Звук при столкновении

            # Проверка взаимодействия с паверапами
            powerup_type = game_map.check_powerup_collision(player.hitbox)
            if powerup_type:
                audio.play_sound(powerup_type)
                if powerup_type == "speed":
                    player.increase_max_speed(1.5)  # Увеличиваем скорость на 50% на 7 секунд
                elif powerup_type == "score":
                    player.increase_max_speed(1.05)  # Увеличиваем скорость на 5% на 7 секунд
                elif powerup_type == "shield":
                    pass  # Логика щита
                elif powerup_type == "oil":
                    pass  # Логика масла

            # Генерация новых паверапов
            current_time = time.time()
            if current_time - last_powerup_spawn_time > POWERUP_SPAWN_INTERVAL:
                # Подсчет текущего количества каждого типа паверапов
                powerup_counts = {"score": 0, "speed": 0, "shield": 0, "oil": 0}
                for p in game_map.powerups:
                    powerup_counts[p.type] += 1

                # Генерация новых паверапов, если их меньше максимального количества
                for powerup_type, max_count in MAX_POWERUPS.items():
                    if powerup_counts[powerup_type] < max_count:
                        x = random.randint(0, MAP_WIDTH)
                        y = random.randint(0, MAP_HEIGHT)                     
                        game_map.powerups.append(PowerUp(powerup_type, x, y))

                last_powerup_spawn_time = current_time  # Обновляем время последней попытки

            # Отрисовка
            screen.fill(BACKGROUND_COLOR)
            game_map.draw(screen, camera)
            player.draw(screen, camera)

            # Отображение скорости
            draw_speed(screen, player.speed)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
    except Exception as e:
        # Логируем ошибку
        error_message = traceback.format_exc()  # Получаем полную трассировку стека
        log_crash(error_message)
        print("Произошла ошибка! Информация записана в crash_report.txt.")
        pygame.quit()


if __name__ == "__main__":
    main()