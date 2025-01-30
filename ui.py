# ui.py
import pygame
from settings import *

class VolumeSlider:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.slider_pos = 100  # Начальная позиция (громкость 50%)
        self.width = 200
        self.height = 20

    def draw(self, screen):
        # Рисуем фон ползунка
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
        # Рисуем сам ползунок
        pygame.draw.circle(screen, (200, 200, 200), (self.x + self.slider_pos, self.y + self.height // 2), 15)

    def update(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width:
            self.slider_pos = mouse_pos[0] - self.x
            self.slider_pos = max(0, min(self.slider_pos, self.width))


class MainMenu:
    def __init__(self, screen, audio_manager):
        self.screen = screen
        self.audio = audio_manager
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.volume_slider = VolumeSlider(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        self.title_text = self.font.render("Car Game", True, (0, 0, 0))
        self.instruction_text = self.small_font.render("Press ENTER to Start", True, (0, 0, 0))
        self.volume_text = self.small_font.render("Volume:", True, (0, 0, 0))

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        # Заголовок
        self.screen.blit(self.title_text, (SCREEN_WIDTH // 2 - self.title_text.get_width() // 2, 100))
        # Инструкция
        self.screen.blit(self.instruction_text, (SCREEN_WIDTH // 2 - self.instruction_text.get_width() // 2, 300))
        # Ползунок громкости
        self.screen.blit(self.volume_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 30))
        self.volume_slider.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.volume_slider.update(pygame.mouse.get_pos())
            self.audio.set_volume(self.volume_slider.slider_pos / 200)


def input_name(screen):
    name = ""
    input_active = True
    font = pygame.font.Font(None, 36)
    while input_active:
        screen.fill(BACKGROUND_COLOR)
        # Текст запроса
        prompt = font.render("Enter your name:", True, (0, 0, 0))
        name_surface = font.render(name, True, (0, 0, 0))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(name_surface, (SCREEN_WIDTH // 2 - name_surface.get_width() // 2, SCREEN_HEIGHT // 2))
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