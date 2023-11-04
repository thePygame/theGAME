import pygame


class HealthBar:
    def __init__(self, game):
        self.game = game
        self.width = game.settings.hpBarWidth * game.scaleX
        self.height = game.settings.hpBarHeight * game.scaleY

        self.fullColor = game.settings.GREEN
        self.emptyColor = game.settings.RED
        self.bordersColor = game.settings.BLACK

    def display_player_hp(self, currentHealth, maxHealth):
        """Wyświetla na środku u dołu ekranu pasek zdrowia gracza."""
        # RED BAR
        x = self.game.screenW / 2 - self.width / 2
        y = self.game.screenH - self.height
        hpBarRed = pygame.Rect((x, y), (self.width, self.height))
        pygame.draw.rect(self.game.screen, self.emptyColor, hpBarRed)
        # GREEN BAR
        procHp = self.width * (currentHealth / maxHealth)
        hpBarGreen = pygame.Rect((x, y), (procHp, self.height))
        pygame.draw.rect(self.game.screen, self.fullColor, hpBarGreen)
        # BLACK BORDER
        pygame.draw.rect(self.game.screen, self.bordersColor, hpBarRed, 2)
