class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize the game's static settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ai_game = ai_game

        # Ship settings.
        self.ship_speed = 0.5
        self.ships_limit = 3
        self.ship_acceleration = 4

        # Bullet settings.
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # How quickly the alien points increase
        self.score_scale = 1.5

        # How quickly the game speeds up.
        self.speedup_scale = 1.2 # 1.2 default

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change in during the game'''
        # Bullet settings.
        self.bullet_speed = 3
        self.bullets_allowed = 3000

        # Alien settings.
        self.alien_speed = 0.2
        self.fleet_direction = 1 # 1=right, -1=left
        self.fleet_drop_speed = 10

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien points values. Every new lvl"""
        if self.ai_game.stats.level <= 3:
            self.alien_speed *= self.speedup_scale
        else:
            # When you reach 5 lvl
            self.bullets_allowed = 2
            self.bullet_width = 3

        self.alien_points = int(self.alien_points * self.score_scale)