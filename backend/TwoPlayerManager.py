from fastapi import WebSocket

class TwoPlayerManager:
    def __init__(self):
        self.players: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        if len(self.players) >= 2:
            await websocket.close(code=1008)
            return False
        await websocket.accept()
        self.players.append(websocket)

        # Send role to the connected player
        role = "X" if len(self.players) == 1 else "O"
        await websocket.send_json({"type": "role", "role": role})
        return True

    def disconnect(self, websocket: WebSocket):
        if websocket in self.players:
            self.players.remove(websocket)

    async def broadcast(self, message: dict):
        for player in self.players:
            await player.send_json(message)
