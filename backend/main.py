from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.TwoPlayerManager import TwoPlayerManager
from backend.game import Game

app = FastAPI()

# CORS configuration
origins = ["http://localhost:5173", "https://four-in-row-pi.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = TwoPlayerManager()
game = Game()


@app.websocket("/ws/game")
async def websocket_endpoint(websocket: WebSocket):
    connected = await manager.connect(websocket)
    if not connected:
        return

    try:
        while True:
            data = await websocket.receive_json()

            if data["action"] == "move":
                player_index = manager.players.index(websocket)
                current_player_index = 0 if game.get_current_player().name == "X" else 1

                if player_index != current_player_index:
                    await websocket.send_json(
                        {"success": False, "message": "Not your turn"}
                    )
                    continue

                success, message = game.play_turn(data["col"])

                await manager.broadcast(
                    {
                        "type": "update",
                        "success": success,
                        "message": message,
                        "board": game.get_board_display().tolist(),
                        "currentPlayer": game.get_current_player().name,
                        "gameOver": game.game_over,
                        "winner": game.get_current_player().name
                        if game.game_over and not game.board.is_full()
                        else "Draw"
                        if game.board.is_full()
                        else None,
                    }
                )

            elif data["action"] == "reset":
                game.reset()
                await manager.broadcast(
                    {
                        "type": "update",
                        "board": game.get_board_display().tolist(),
                        "currentPlayer": game.get_current_player().name,
                        "gameOver": False,
                        "winner": None,
                    }
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/")
def read_root():
    return {"message": "Four in a Row API is running"}


@app.get("/game")
def get_game_state():
    return {
        "board": game.get_board_display().tolist(),
        "currentPlayer": game.get_current_player().name,
        "gameOver": game.game_over,
        "winner": game.get_current_player().name
        if game.game_over and not game.board.is_full()
        else "Draw"
        if game.board.is_full()
        else None,
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
        "winner": game.get_current_player().name
        if game.game_over and not game.board.is_full()
        else "Draw"
        if game.board.is_full()
        else None,
    }


@app.post("/game/reset")
def reset_game():
    game.reset()
    return {
        "board": game.get_board_display().tolist(),
        "currentPlayer": game.get_current_player().name,
        "gameOver": game.game_over,
        "winner": None,
    }
