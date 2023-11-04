class Settings:
    """Klasa przechowująca kluczowe dane dla działania programu."""

    def __init__(self):
        self.game_title = "Runner"
        self.screenWidth = 1280
        self.screenHeight = 720
        self.fps = 60
        self.fontSize = 50
        # KOLORY.
        self.themeColor = (94, 129, 162)
        self.fontColor = (111, 196, 169)
        self.BLACK = (0, 0, 0)
        self.RED = (200, 0, 0)
        self.GREEN = (0, 150, 0)
        # GRACZ
        self.playerHealth = 50
        self.playerSpeed = 10
        self.playerJump = -20
        self.hpBarWidth = 300
        self.hpBarHeight = 30
        # PRZESZKODY.
        self.enemySpeed = 6
        self.enemyDamage = -10
        self.enemyPoints = 5
        self.bananaHeal = 5
        # Czas mierzony w milisekundach od zaczęcia gry do momentu pomiaru,
        # dzielony jest przez tę liczbę dając przebyty przez gracza "dystans".
        self.distanceSpeed = 50
