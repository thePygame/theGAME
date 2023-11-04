import pygame
import useful


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        player_walk_1 = useful.load_scale_image(
            "graphics/player/sprite_cuteknight1.png",
            game.scale_x, game.scale_y, 1)
        player_walk_2 = useful.load_scale_image(
            "graphics/player/sprite_cuteknight2.png",
            game.scale_x, game.scale_y, 1)
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = useful.load_scale_image(
            "graphics/player/sprite_knight_jump.png",
            game.scale_x, game.scale_y, 1)
        self.image = self.player_walk[self.player_index]
        self.player_y = game.ground_y - self.image.get_height()
        self.rect = self.image.get_rect(
            midbottom=(80 * game.scale_x, self.player_y))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
        self.speed = game.settings.player_speed
        self.jump = game.settings.player_jump
        self.max_health = self.game.settings.player_health
        self.current_health = self.game.settings.player_health
        self.hp_bar_w = game.settings.hp_bar_width * game.scale_x
        self.hp_bar_h = game.settings.hp_bar_height * game.scale_y

    def reset(self):
        self.current_health = self.max_health
        self.rect = self.image.get_rect(
            midbottom=(80 * self.game.scale_x, self.player_y))

    def take_damage(self, damage):
        if self.current_health + damage <= self.max_health:
            self.current_health += damage

    def _display_player_hp(self):
        """Wyświetla na środku na dole ekranu pasek zdrowia gracza."""
        # RED BAR
        x = self.game.screen_w / 2 - self.hp_bar_w / 2
        y = self.game.screen_h - self.hp_bar_h
        hp_bar_red = pygame.Rect((x, y), (self.hp_bar_w, self.hp_bar_h))
        pygame.draw.rect(self.game.screen, self.game.settings.RED, hp_bar_red)
        # GREEN BAR
        proc_hp = self.hp_bar_w * (self.current_health / self.max_health)
        hp_bar_green = pygame.Rect((x, y), (proc_hp, self.hp_bar_h))
        pygame.draw.rect(self.game.screen, self.game.settings.GREEN,
                         hp_bar_green)
        # BLACK BORDER
        pygame.draw.rect(self.game.screen, self.game.settings.BLACK,
                         hp_bar_red, 2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.game.ground_y:
            self.gravity = self.jump
            self.jump_sound.play()
        if keys[pygame.K_d] and self.rect.right <= self.game.screen.get_width():
            self.rect.x += self.speed
        if keys[pygame.K_a] and self.rect.left >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_s] and self.rect.left >= 0:
            self.rect.y += self.speed

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.game.ground_y:
            self.rect.bottom = self.game.ground_y

    def animation_state(self):
        if self.rect.bottom < self.game.ground_y:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self._display_player_hp()
        self.player_input()
        self.apply_gravity()
        self.animation_state()
