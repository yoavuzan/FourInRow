from fastapi import WebSocket

class TwoPlayerManager:
    def __init__(self):
        self.players: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        if len(self.players) >= 2:
            await ws.close(code=1000)
            return False
        await ws.accept()
        self.players.append(ws)
        return True

    def disconnect(self, ws: WebSocket):
        if ws in self.players:
            self.players.remove(ws)

    async def broadcast(self, data: dict):
        for p in self.players:
            await p.send_json(data)
