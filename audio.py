# audio.py
import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "score": pygame.mixer.Sound("resources/score.wav"),
            "speed": pygame.mixer.Sound("resources/speed.wav"),
            "shield": pygame.mixer.Sound("resources/shield.wav"),
            "oil": pygame.mixer.Sound("resources/oil.wav")
        }
        pygame.mixer.music.load("resources/background_music.mp3")
        self.volume = 0.1

    def play_music(self):
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume)

    def play_sound(self, name):
        self.sounds[name].set_volume(self.volume)
        self.sounds[name].play()

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)