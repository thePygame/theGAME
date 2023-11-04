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
            self.damage = game.settings.enemyDamage
            self.points = game.settings.enemyPoints
            yPos = 0 + self.frames[0].get_height()
        elif type == "snail":
            self._load_imgs(type)
            self.damage = game.settings.enemyDamage
            self.points = game.settings.enemyPoints
            yPos = game.groundY
        elif type == "banana":
            self._load_imgs(type)
            self.damage = game.settings.bananaHeal
            self.points = 0
            yPos = game.groundY

        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom=(
            randint(int(game.screenW * 1.2), int(game.screenW * 1.6)), yPos))

    def _load_imgs(self, type):
        """Funkcja ładująca obrazy do animacji dla sprite'a znajdujące się w
        bibliotece /graphics o nazwie sprite_typei, gdzie i to numer klatki."""

        folderPath = f"graphics/{type}"
        fileCount = len(os.listdir(folderPath))
        for i in range(fileCount):
            img = pygame.image.load(f"{folderPath}/sprite_{type}"
                                    f"{i + 1}.png").convert_alpha()
            img = useful.scale_image(img, self.game.scaleX, self.game.scaleY)
            self.frames.append(img)

    def _animation_state(self):
        self.animationIndex += 0.05
        if self.animationIndex >= len(self.frames): self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def _destroy(self):
        if self.rect.right <= 0:
            self.game.statistics.score += self.points
            self.kill()

    def update(self):
        self._animation_state()
        self.rect.x -= self.game.settings.enemySpeed
        self._destroy()
