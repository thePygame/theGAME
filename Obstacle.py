import os

import pygame
from random import randint

import useful


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, type):
        super().__init__()
        self.game = game
        self.type = type
        self.frames = []

        if type == 'storm':
            self._load_imgs(type)
            self.damage = game.settings.enemy_damage
            self.points = game.settings.enemy_points
            y_pos = 0 + self.frames[0].get_height()
        elif type == "snail":
            self._load_imgs(type)
            self.damage = game.settings.enemy_damage
            self.points = game.settings.enemy_points
            y_pos = game.ground_y
        elif type == "banana":
            self._load_imgs(type)
            self.damage = game.settings.banana_heal
            self.points = 0
            y_pos = game.ground_y

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(
            randint(int(game.screen_w * 1.2), int(game.screen_w * 1.6)),
            y_pos))

    def _load_imgs(self, type):
        """Funkcja ładująca obrazy do animacji dla sprite'a znajdujące się w
        bibliotece /graphics o nazwie sprite_type_i, gdzie i to numer klatki."""

        folder_path = f"graphics/{type}"
        file_count = len(os.listdir(folder_path))
        for i in range(2):
            img = pygame.image.load(f"{folder_path}/sprite_{type}{i + 1}.png").convert_alpha()
            img = useful.scale_image(img, self.game.scale_x, self.game.scale_y)
            self.frames.append(img)

    def animation_state(self):
        self.animation_index += 0.05
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.game.settings.enemy_speed
        self._destroy()

    def _destroy(self):
        if self.rect.right <= 0:
            self.game.statistics.score += self.points
            self.kill()
