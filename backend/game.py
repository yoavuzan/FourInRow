from backend.board import Board
from backend.player import Player

class Game:
    def __init__(self, rows=6, cols=7):
        self.board = Board(rows, cols)
        self.players = [Player("Player 1", 'X'), Player("Player 2", 'O')]
        self.current_player_index = 0
        self.game_over = False

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % 2

    def get_current_player(self):
        return self.players[self.current_player_index]

    def play_turn(self, col):
        if self.game_over:
            return False, "Game is over."

        if not self.board.is_valid_location(col):
            return False, "Invalid column. Please choose another one."

        row = self.board.get_next_open_row(col)
        piece = self.get_current_player().symbol
        self.board.drop_piece(row, col, piece)

        if self.board.check_win(piece):
            self.game_over = True
            return True, f"{self.get_current_player().name} wins!"

        if self.board.is_full():
            self.game_over = True
            return True, "The game is a draw!"

        self.switch_player()
        return True, ""

    def get_board_display(self):
        # This can be enhanced for different UIs
        return self.board.board
    
    def reset(self):
        self.board = Board(self.board.rows, self.board.cols)
        self.current_player_index = 0
        self.game_over = False