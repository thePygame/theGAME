import pygame
from settings import Settings
from statistics import Statistics
from player import Player
from obstacle import Obstacle
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
        self.screenW = self.settings.screenWidth
        self.screenH = self.settings.screenHeight
        self.fontSize = self.settings.fontSize
        self.screen = pygame.display.set_mode((self.screenW, self.screenH))
        pygame.display.set_caption(self.settings.game_title)
        self.clock = pygame.time.Clock()
        self.gameRunning = False
        self.startTime = 0
        self.hs = self.statistics.hs

        # Resources.
        self.bgMusic = pygame.mixer.Sound('audio/Hoppin.mp3')
        self.bgMusic.play(loops=-1)
        self.bgMusic.set_volume(0.1)
        self.bgImg = pygame.image.load('graphics/morninghill.png').convert()

        self.scaleX, self.scaleY = useful.get_scale(self.screen, self.bgImg)
        self.bgImg = useful.scale_image(self.bgImg, self.scaleX,
                                        self.scaleY)
        self.groundImg = useful.load_scale_image("graphics/ground.png",
                                                 self.scaleX, self.scaleY)
        self.groundY = self.screen.get_height() - self.groundImg.get_height()

        self.font = pygame.font.Font('font/Pixeltype.ttf',
                                     int(self.fontSize * self.scaleX))
        self.titleFont = pygame.font.Font('font/Pixeltype.ttf',
                                          int(self.fontSize * 2 *
                                              self.scaleX))

        # Groups
        self.banana = Obstacle(self, "banana")
        self.bananas = pygame.sprite.GroupSingle()
        self.bananas.add(self.banana)
        self.player = Player(self)
        self.players = pygame.sprite.GroupSingle()
        self.players.add(self.player)
        self.obstacles = pygame.sprite.Group()

        # Intro screen
        self.startImg = useful.load_scale_image(
            "graphics/player/sprite_knight_stand.png",
            self.scaleX, self.scaleY, 1)
        self.startImg = pygame.transform.rotozoom(self.startImg, 0, 2)
        self.startImgRect = self.startImg.get_rect(
            center=self.screen.get_rect().center)

        self.title_msg = self.titleFont.render(self.settings.game_title, True,
                                               self.settings.fontColor)
        self.title_msg_rect = self.title_msg.get_rect(
            midbottom=(self.screenW / 2, self.startImgRect.top))

        self.start_msg = self.font.render('Press space to jump', True,
                                          self.settings.fontColor)
        self.start_msg_rect = self.start_msg.get_rect(
            midtop=(self.screenW / 2,
                    self.startImgRect.bottom + self.start_msg.get_rect().h))

        # Timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

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
                    self.player.currentHealth = 0
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
                    self.startTime = pygame.time.get_ticks()

    def _check_collision(self):
        for obstacle in self.obstacles:
            if obstacle.rect.colliderect(self.player.rect):
                self.player.take_damage(obstacle.damage)
                if obstacle.type == "banana":
                    self.statistics.bananas += 1
                obstacle.kill()
            if self.player.currentHealth <= 0:
                self.statistics.compare()
                self.statistics.load_highs()
                self.gameRunning = False

    def _update_screen(self):
        # Tło.
        self.screen.blit(self.bgImg, (0, 0))
        self.screen.blit(self.groundImg, (0, self.groundY))
        # UI.
        self._display_score()
        self._display_distance()
        self._display_time()
        # Sprite'y.
        self.players.update()
        self.players.draw(self.screen)
        self.obstacles.update()
        self.obstacles.draw(self.screen)

    def _display_score(self):
        # current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        scoreSurf = self.font.render(f'Score: {self.statistics.score}', True,
                                     self.settings.BLACK)
        scoreRect = scoreSurf.get_rect(
            topright=(self.screenW, 0))
        self.screen.blit(scoreSurf, scoreRect)

    def _display_distance(self):
        distance = (pygame.time.get_ticks() - self.startTime)
        distance //= self.settings.distanceSpeed
        distanceMsg = self.font.render(f'Distance: {distance}m', True,
                                       self.settings.BLACK)
        distanceMsgRect = distanceMsg.get_rect(
            midtop=(self.screenW / 2, 0))
        self.statistics.distance = distance
        self.screen.blit(distanceMsg, distanceMsgRect)

    def _display_time(self):
        time = pygame.time.get_ticks() // 1000
        timeMsg = self.font.render(f"Time: {time}", True, self.settings.BLACK)
        timeMsgRect = timeMsg.get_rect(
            bottomright=(self.screenW, self.screenH))
        self.screen.blit(timeMsg, timeMsgRect)

    def _display_start_screen(self):
        self.screen.fill(self.settings.themeColor)
        self.screen.blit(self.startImg, self.startImgRect)
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
            self.settings.fontColor)
        scoreMsgRect = score_msg.get_rect(
            midtop=(self.screenW / 2,
                    self.startImgRect.bottom + score_msg.get_rect().h))
        self.screen.blit(score_msg, scoreMsgRect)

    def _display_start_bananas(self):
        # Banan z lewej.
        self.banana.rect.midleft = (2 * self.banana.rect.w, self.screenH / 2)
        self.banana.update()
        self.bananas.draw(self.screen)
        # Zmiana rect banana i napisanie tekstu.
        self.banana.rect.midleft = (3 * self.banana.rect.w, self.screenH / 2)
        bananasMsg = self.font.render(str(self.statistics.hb), True,
                                      self.settings.fontColor)
        bananasMsgRect = bananasMsg.get_rect(
            center=(self.banana.rect.centerx, self.banana.rect.centery))
        self.screen.blit(bananasMsg, bananasMsgRect)
        # Banan z prawej.
        self.banana.rect.midleft = (4 * self.banana.rect.w, self.screenH / 2)
        self.bananas.draw(self.screen)

    def _display_start_distance(self):
        distanceMsg = self.font.render(f"Distance: {self.statistics.hd}m",
                                       True, self.settings.fontColor)
        distanceMsgRect = distanceMsg.get_rect(
            midright=(self.screenW - self.banana.rect.w, self.screenH / 2))
        self.screen.blit(distanceMsg, distanceMsgRect)

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
