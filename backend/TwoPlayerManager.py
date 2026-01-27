from fastapi.websockets import WebSocket
class TwoPlayerManager:
    def __init__(self):
        self.players: list[WebSocket] = []
        self.roles: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket):
        if len(self.players) >= 2:
            await websocket.close(code=1008)
            return False
        await websocket.accept()
        self.players.append(websocket)
        role = "X" if len(self.players) == 1 else "O"
        self.roles[websocket] = role
        await websocket.send_json({"type": "role", "role": role})
        return True

    def disconnect(self, websocket: WebSocket):
        if websocket in self.players:
            self.players.remove(websocket)
            self.roles.pop(websocket, None)

    def get_role(self, websocket: WebSocket):
        return self.roles.get(websocket)

    async def broadcast(self, message: dict):
        for player in self.players:
            await player.send_json(message)
