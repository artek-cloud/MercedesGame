import pygame
from settings import *

def input_name(screen):
    name = ""
    input_active = True
    font = pygame.font.Font(None, 36)

    while input_active:
        screen.fill(SKY_BLUE)
        prompt = font.render("Enter your name:", True, BLACK)
        name_display = font.render(name, True, BLACK)
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(name_display, (SCREEN_WIDTH//2 - name_display.get_width()//2, SCREEN_HEIGHT//2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return name

def main_menu(screen, sound_enabled):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    title = font.render("Mercedes Benz GLK Snake Game", True, BLACK)
    play_text = small_font.render("Press ENTER to Start", True, BLACK)
    sound_text = small_font.render(f"Sound: {'ON' if sound_enabled else 'OFF'} (Press S)", True, BLACK)

    while True:
        screen.fill(SKY_BLUE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        screen.blit(play_text, (SCREEN_WIDTH//2 - play_text.get_width()//2, 300))
        screen.blit(sound_text, (SCREEN_WIDTH//2 - sound_text.get_width()//2, 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return sound_enabled
                elif event.key == pygame.K_s:
                    sound_enabled = not sound_enabled
                    sound_text = small_font.render(
                        f"Sound: {'ON' if sound_enabled else 'OFF'} (Press S)", 
                        True, 
                        BLACK
                    )

def show_leaderboard(screen):
    try:
        with open("leaderboard.txt", "r") as file:
            leaderboard_data = file.readlines()
    except FileNotFoundError:
        leaderboard_data = ["Таблица лидеров пуста."]

    screen.fill(SKY_BLUE)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Таблица лидеров", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    y_offset = 100
    for line in leaderboard_data:
        line = line.strip()
        text = font.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40

    pygame.display.flip()
    pygame.time.wait(3000)

def game_over_screen(screen, score):
    screen.fill(SKY_BLUE)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, BLACK)
    score_text = font.render(f"Your Score: {score}", True, BLACK)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))

    pygame.display.flip()
    pygame.time.wait(3000)
    return True