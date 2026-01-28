class Player:
    def __init__(self, name, symbol, score=0):
        self.name = name
        self.symbol = symbol
        self.score = score

    def update_score(self, points):
        self.score += points

    def get_info(self):
        return {"name": self.name, "symbol": self.symbol, "score": self.score}
    
    def get_symbol(self):
        return self.symbol
class AIPlayer(Player):
    def __init__(self, name, symbol, difficulty="medium", score=0):
        super().__init__(name, symbol, score)
        self.difficulty = difficulty

    # AI-specific logic would go here
    def make_move(self, board):
        # This is a placeholder for AI move logic
        pass