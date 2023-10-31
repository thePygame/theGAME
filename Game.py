import pygame
from Settings import Settings
from Statistics import Statistics
from Player import Player
from Obstacle import Obstacle
import useful

from random import choice

pygame.font.init()
pygame.mixer.init()


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

        self.scale_x, self.scale_y = useful.get_scale(self.screen, self.bg_img)
        self.bg_img = useful.scale_image(self.bg_img, self.scale_x,
                                         self.scale_y)
        self.ground_img = useful.load_scale_image("graphics/ground.png",
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
        self.start_img = useful.load_scale_image(
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
