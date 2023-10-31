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
