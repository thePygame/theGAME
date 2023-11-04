import pygame
import useful
from health_bar import HealthBar


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        playerWalk1 = useful.load_scale_image(
            "graphics/player/sprite_cuteknight1.png",
            game.scaleX, game.scaleY, 1)
        playerWalk2 = useful.load_scale_image(
            "graphics/player/sprite_cuteknight2.png",
            game.scaleX, game.scaleY, 1)
        self.playerWalk = [playerWalk1, playerWalk2]
        self.playerJump = useful.load_scale_image(
            "graphics/player/sprite_knight_jump.png",
            game.scaleX, game.scaleY, 1)
        self.playerIndex = 0
        self.image = self.playerWalk[self.playerIndex]
        self.playerY = game.groundY - self.image.get_height()
        self.rect = self.image.get_rect(
            midbottom=(80 * game.scaleX, self.playerY))

        self.jumpSound = pygame.mixer.Sound('audio/jump.mp3')
        self.jumpSound.set_volume(0.5)

        self.healthBar = HealthBar(game)

        self.maxHealth = self.game.settings.playerHealth
        self.currentHealth = self.game.settings.playerHealth
        self.speed = game.settings.playerSpeed
        self.jump = game.settings.playerJump
        self.gravity = 0

    def reset(self):
        self.currentHealth = self.maxHealth
        self.rect = self.image.get_rect(
            midbottom=(80 * self.game.scaleX, self.playerY))

    def take_damage(self, damage):
        if self.currentHealth + damage <= self.maxHealth:
            self.currentHealth += damage

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.game.groundY:
            self.gravity = self.jump
            self.jumpSound.play()
        if keys[pygame.K_d] and self.rect.right <= self.game.screen.get_width():
            self.rect.x += self.speed
        if keys[pygame.K_a] and self.rect.left >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_s] and self.rect.left >= 0:
            self.rect.y += self.speed

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.game.groundY:
            self.rect.bottom = self.game.groundY

    def animation_state(self):
        if self.rect.bottom < self.game.groundY:
            self.image = self.playerJump
        else:
            self.playerIndex += 0.1
            if self.playerIndex >= len(self.playerWalk):
                self.playerIndex = 0
            self.image = self.playerWalk[int(self.playerIndex)]

    def update(self):
        self.healthBar.display_player_hp(self.currentHealth, self.maxHealth)
        self.player_input()
        self.apply_gravity()
        self.animation_state()
