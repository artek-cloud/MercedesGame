# main.py
import pygame
from settings import *
from camera import Camera
from map import GameMap
from player import Player
from audio import AudioManager
from ui import MainMenu, input_name

def main():
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
            player.speed *= -2  # Отталкивание игрока
            audio.play_sound("shield")  # Звук при столкновении

        # Проверка взаимодействия с паверапами
        powerup_type = game_map.check_powerup_collision(player.hitbox)
        if powerup_type:
            audio.play_sound(powerup_type)
            if powerup_type == "speed":
                player.speed *= 1.5  # Увеличение скорости на 50%
            elif powerup_type == "shield":
                pass  # Логика щита (можно добавить позже)
            elif powerup_type == "oil":
                pass  # Логика масла (можно добавить позже)

        # Отрисовка
        screen.fill(BACKGROUND_COLOR)
        game_map.draw(screen, camera)
        player.draw(screen, camera)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()