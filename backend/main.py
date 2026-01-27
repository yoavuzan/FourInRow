

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from backend.game import Game

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173", 
    "https://four-in-row-pi.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


game = Game()

@app.get("/")
def read_root():
    return {"message": "Four in a Row API is running"}

@app.get("/game")
def get_game_state():
    return {
        "board": game.get_board_display().tolist(),
        "currentPlayer": game.get_current_player().name,
        "gameOver": game.game_over,
        "winner": game.get_current_player().name if game.game_over and not game.board.is_full() else "Draw" if game.board.is_full() else None,
    }

@app.post("/game/move")
def make_move(data: dict):
    col = data.get("col")
    success, message = game.play_turn(col)
    if not success:
        return {"success": False, "message": message}
    
    return {
        "success": True,
        "board": game.get_board_display().tolist(),
        "currentPlayer": game.get_current_player().name,
        "gameOver": game.game_over,
        "winner": game.get_current_player().name if game.game_over and not game.board.is_full() else "Draw" if game.board.is_full() else None,
    }

@app.post("/game/reset")
def reset_game():
    global game
    game = Game()
    return {
        "board": game.get_board_display().tolist(),
        "currentPlayer": game.get_current_player().name,
        "gameOver": game.game_over,
        "winner": None,
    }
