# audio.py
import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self._load_sounds()
        pygame.mixer.music.load("resources/background_music.mp3")
        self.volume = 0.1

    def _load_sounds(self):
        sound_files = ["score", "speed", "shield", "oil"]
        for name in sound_files:
            try:
                self.sounds[name] = pygame.mixer.Sound(f"resources/{name}.wav")
            except FileNotFoundError:
                print(f"Ошибка: файл {name}.wav не найден!")
                self.sounds[name] = pygame.Surface((0, 0))

    def play_music(self):
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume)

    def play_sound(self, name):
        self.sounds[name].set_volume(self.volume)
        self.sounds[name].play()

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)