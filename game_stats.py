class GameStats():
    """check game stats"""

    def __init__(self, ai_settings):
        """init stats"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # game active flag
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """init geme stats"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
       