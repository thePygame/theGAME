import pygame

from random import choice
from random import randint
import os
import json

pygame.font.init()
pygame.mixer.init()


def get_scale(screen: pygame.surface.Surface, image: pygame.surface.Surface):
    # szerokość okna / oryginalna szerokość obrazka
    scale_x = screen.get_width() / image.get_width()
    scale_y = screen.get_height() / image.get_height()
    return scale_x, scale_y


def scale_image(image: pygame.surface.Surface, scale_x, scale_y):
    """Funkcja skaluje podany obraz image przez wartości skali scale_x i
    scale_y."""
    _image = pygame.transform.scale(image,
                                    (image.get_width() * scale_x,
                                     image.get_height() * scale_y))
    return _image


def load_scale_image(path, scale_x, scale_y, convert_alpha=0):
    """Funkcja wczytuje z podanej ścierzki path obraz i skaluje go przez
    podane skale scale_x i scale_y."""
    path = path
    if not convert_alpha:
        img = pygame.image.load(path).convert()
    elif convert_alpha:
        img = pygame.image.load(path).convert_alpha()
    img = scale_image(img, scale_x, scale_y)
    return img


class Statistics:
    """Klasa przechowująca dane statystyczne gracza."""

    def __init__(self):
        self.score = 0
        self.distance = 0
        self.bananas = 0
        self.hs = self.load_hs("SCORE")
        self.hd = self.load_hs("DISTANCE")
        self.hb = self.load_hs("BANANAS")

    def reset(self):
        """Tworzy domyślne zmienne klasy."""
        self.score = 0
        self.distance = 0
        self.bananas = 0
        self.load_highs()

    def load_highs(self):
        self.hs = self.load_hs("SCORE")
        self.hd = self.load_hs("DISTANCE")
        self.hb = self.load_hs("BANANAS")

    def compare(self):
        """Porównuje najlepszy wynik do aktualnie uzyskanego. Jeżeli jest
        większy zostaje podmieniony w pliku data.json."""
        if self.hs < self.score:
            self.save_hs(self.score, self.distance, self.bananas)

    def load_hs(self, type="SCORE"):
        """Wczytuje plik data.json z najwyższym wynikiem. Jeżeli taki
        istnieje zwraca trzy wartości kolejno: score, distance, bananas.
        Jeżeli taki nie istnieje, tworzy go z wartościami 0, 0, 0."""
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                for i in data:
                    if i == type:
                        return data[i]
                f.close()
        except FileNotFoundError:
            self.save_hs(0, 0, 0)

    def save_hs(self, score, distance, bananas):
        """Zapisuje najwyższy wynik do pliku data.json."""
        with open("data.json", "w") as f:
            text = {"SCORE": score,
                    "DISTANCE": distance,
                    "BANANAS": bananas}
            json.dump(text, f)
            f.close()


class Settings:
    """Klasa przechowująca kluczowe dane dla działania programu."""

    def __init__(self):
        self.game_title = "Runner"
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60
        self.font_size = 50

        self.theme_color = (94, 129, 162)
        self.font_color = (111, 196, 169)
        self.BLACK = (0, 0, 0)
        self.RED = (200, 0, 0)
        self.GREEN = (0, 150, 0)

        self.player_health = 50
        self.player_speed = 10
        self.player_jump = -20
        self.hp_bar_width = 300
        self.hp_bar_height = 30

        self.distance_speed = 50
        self.enemy_speed = 6

        self.enemy_damage = -10
        self.enemy_points = 5
        self.banana_heal = 5


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
        bibliotece /graphics o nazwie sprite_typei, gdzie i to numer klatki."""

        folder_path = f"graphics/{type}"
        file_count = len(os.listdir(folder_path))
        for i in range(file_count):
            img = pygame.image.load(f"{folder_path}/sprite_{type}"
                                    f"{i + 1}.png").convert_alpha()
            img = scale_image(img, self.game.scale_x, self.game.scale_y)
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


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        player_walk_1 = load_scale_image(
            "graphics/player/sprite_cuteknight1.png",
            game.scale_x, game.scale_y, 1)
        player_walk_2 = load_scale_image(
            "graphics/player/sprite_cuteknight2.png",
            game.scale_x, game.scale_y, 1)
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = load_scale_image(
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


class Game:
    def __init__(self):
        # pygame.init()
        self.isRunning = True
        self.settings = Settings()
        self.statistics = Statistics()
        self.screen_w = self.settings.screen_width
        self.screen_h = self.settings.screen_height
        self.font_size = self.settings.font_size
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption(self.settings.game_title)
        self.clock = pygame.time.Clock()
        self.gameRunning = False
        self.start_time = 0
        self.hs = self.statistics.hs

        # Resources.
        self.bg_music = pygame.mixer.Sound('audio/Hoppin.mp3')
        self.bg_music.play(loops=-1)
        self.bg_img = pygame.image.load('graphics/morninghill.png').convert()

        self.scale_x, self.scale_y = get_scale(self.screen, self.bg_img)
        self.bg_img = scale_image(self.bg_img, self.scale_x,
                                  self.scale_y)
        self.ground_img = load_scale_image("graphics/ground.png",
                                           self.scale_x, self.scale_y)
        self.ground_y = self.screen.get_height() - self.ground_img.get_height()

        self.font = pygame.font.Font('font/Pixeltype.ttf',
                                     int(self.font_size * self.scale_x))
        self.title_font = pygame.font.Font('font/Pixeltype.ttf',
                                           int(self.font_size * 2 *
                                               self.scale_x))

        # Groups
        self.banana = Obstacle(self, "banana")
        self.bananas = pygame.sprite.GroupSingle()
        self.bananas.add(self.banana)
        self.player = Player(self)
        self.players = pygame.sprite.GroupSingle()
        self.players.add(self.player)
        self.obstacles = pygame.sprite.Group()

        # Intro screen
        self.start_img = load_scale_image(
            "graphics/player/sprite_knight_stand.png",
            self.scale_x, self.scale_y, 1)
        self.start_img = pygame.transform.rotozoom(self.start_img, 0, 2)
        self.start_img_rect = self.start_img.get_rect(
            center=self.screen.get_rect().center)

        self.title_msg = self.title_font.render(self.settings.game_title, True,
                                                self.settings.font_color)
        self.title_msg_rect = self.title_msg.get_rect(
            midbottom=(self.screen_w / 2, self.start_img_rect.top))

        self.start_msg = self.font.render('Press space to jump', True,
                                          self.settings.font_color)
        self.start_msg_rect = self.start_msg.get_rect(
            midtop=(self.screen_w / 2,
                    self.start_img_rect.bottom + self.start_msg.get_rect().h))

        # Timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

    def _display_start_screen(self):
        self.screen.fill(self.settings.theme_color)
        self.screen.blit(self.start_img, self.start_img_rect)
        self.screen.blit(self.title_msg, self.title_msg_rect)
        if self.statistics.score == 0:
            self.screen.blit(self.start_msg, self.start_msg_rect)
        else:
            self._display_start_highscore()
            self._display_start_bananas()
            self._display_start_distance()

    def _display_start_highscore(self):
        score_msg = self.font.render(
            f'Highest score: {self.statistics.hs}', True,
            self.settings.font_color)
        score_msg_rect = score_msg.get_rect(
            midtop=(self.screen_w / 2,
                    self.start_img_rect.bottom + score_msg.get_rect().h))
        self.screen.blit(score_msg, score_msg_rect)

    def _display_start_bananas(self):
        # Banan z lewej.
        self.banana.rect.midleft = (2 * self.banana.rect.w, self.screen_h / 2)
        self.banana.update()
        self.bananas.draw(self.screen)
        # Zmiana rect banana i napisanie tekstu.
        self.banana.rect.midleft = (3 * self.banana.rect.w, self.screen_h / 2)
        bananas_msg = self.font.render(str(self.statistics.hb), True,
                                       self.settings.font_color)
        bananas_msg_rect = bananas_msg.get_rect(
            center=(self.banana.rect.centerx, self.banana.rect.centery))
        self.screen.blit(bananas_msg, bananas_msg_rect)
        # Banan z prawej.
        self.banana.rect.midleft = (4 * self.banana.rect.w, self.screen_h / 2)
        self.bananas.draw(self.screen)

    def _display_start_distance(self):
        distance_msg = self.font.render(f"Distance: {self.statistics.hd}m",
                                        True, self.settings.font_color)
        distance_msg_rect = distance_msg.get_rect(
            midright=(self.screen_w - self.banana.rect.w, self.screen_h / 2))
        self.screen.blit(distance_msg, distance_msg_rect)

    def _display_time(self):
        time = pygame.time.get_ticks() // 1000
        time_msg = self.font.render(f"Time: {time}", True, self.settings.BLACK)
        time_msg_rect = time_msg.get_rect(
            bottomright=(self.screen_w, self.screen_h))
        self.screen.blit(time_msg, time_msg_rect)

    def _display_distance(self):
        distance = (pygame.time.get_ticks() - self.start_time)
        distance //= self.settings.distance_speed
        distance_msg = self.font.render(f'Distance: {distance}m', True,
                                        self.settings.BLACK)
        distance_msg_rect = distance_msg.get_rect(
            midtop=(self.screen_w / 2, 0))
        self.statistics.distance = distance
        self.screen.blit(distance_msg, distance_msg_rect)

    def _display_score(self):
        # current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        score_surf = self.font.render(f'Score: {self.statistics.score}', True,
                                      self.settings.BLACK)
        score_rect = score_surf.get_rect(
            topright=(self.screen_w, 0))
        self.screen.blit(score_surf, score_rect)

    def _check_collision(self):
        for obstacle in self.obstacles:
            if obstacle.rect.colliderect(self.player.rect):
                self.player.take_damage(obstacle.damage)
                if obstacle.type == "banana":
                    self.statistics.bananas += 1
                obstacle.kill()
            if self.player.current_health <= 0:
                self.statistics.compare()
                self.statistics.load_highs()
                self.gameRunning = False

    def _update_screen(self):
        # Grafika.
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.ground_img, (0, self.ground_y))
        # UI.
        self._display_score()
        self._display_distance()
        self._display_time()
        # Sprite'y.
        self.players.update()
        self.players.draw(self.screen)
        self.obstacles.update()
        self.obstacles.draw(self.screen)

    def _reset_game(self):
        self.obstacles.empty()
        self.player.reset()
        self.statistics.reset()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                # DO TESTÓW
                if event.key == pygame.K_KP0:  # NUM0 kys
                    self.player.current_health = 0
                if event.key == pygame.K_KP1:  # NUM1 ślimak
                    self.obstacles.add(Obstacle(self, "snail"))
                if event.key == pygame.K_KP2:  # NUM2 tornado
                    self.obstacles.add(Obstacle(self, "storm"))
                if event.key == pygame.K_KP3:  # NUM3 BANAN
                    self.obstacles.add(Obstacle(self, "banana"))
                if event.key == pygame.K_KP4:  # NUM4 +POINT
                    self.statistics.score += 1

            if self.gameRunning:
                if event.type == self.obstacle_timer:
                    type = choice(
                        ['storm', 'snail', 'snail', 'snail', "banana"])
                    self.obstacles.add(Obstacle(self, type))
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self._reset_game()
                    self.gameRunning = True
                    self.start_time = pygame.time.get_ticks()

    def run(self):
        while self.isRunning:
            self._check_events()
            if self.gameRunning:
                self._check_collision()
                self._update_screen()
            else:
                self._display_start_screen()
            self.clock.tick(self.settings.fps)
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    Game().run()