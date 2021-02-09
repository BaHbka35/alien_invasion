import json

class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in inactive state.
        self.game_active = False

        # High score should never be reset.
        with open('High_score.json') as f:
            self.high_score = json.load(f)

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ships_limit
        self.score = 0 
        self.level = 1

    def update_high_score(self):
        """Update high score."""
        with open('High_score.json', 'w') as f:
            json.dump(self.high_score, f)