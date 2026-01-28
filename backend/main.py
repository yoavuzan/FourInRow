from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.TwoPlayerManager import TwoPlayerManager
from backend.game import Game
import uvicorn

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

    role = manager.get_role(websocket)
    print(f"Player with role {role} connected.")
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            if action == "move":
                player_role = manager.get_role(websocket)[0]
                if player_role != game.get_current_player().symbol:
                    await websocket.send_json(
                        {"success": False, "message": "Not your turn!"}
                    )
                    continue

                col = data.get("col")
                success, message = game.play_turn(col)

                response = {
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
                await manager.broadcast(response)

            elif action == "reset":
                game.reset()
                response = {
                    "type": "update",
                    "board": game.get_board_display().tolist(),
                    "currentPlayer": game.get_current_player().name,
                    "gameOver": False,
                    "winner": None,
                }
                await manager.broadcast(response)

    except WebSocketDisconnect:
        role_left = manager.disconnect(websocket)
        game.reset()
        await manager.broadcast(
            {
                "type": "error",
                "message": f"Player {role_left} left the game. Board reset.",
            }
        )


@app.get("/")
async def root():
    return {"message": "Welcome to the Four in a Row Game API!"}
