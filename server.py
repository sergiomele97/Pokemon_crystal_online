import asyncio
import websockets


class ServerConnection:

    uri = "ws://strategic-kathie-pokemon-crystal-online-d82f6033.koyeb.app"

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            await asyncio.gather(self.send_position(), self.receive_positions())

    async def send_position(self):
        while True:
            await self.websocket.send("Hola que tal?")
            await asyncio.sleep(0.5)  # Envía la posición cada medio segundo

    async def receive_positions(self):
        while True:
            response = await self.websocket.recv()
            print(f"Respuesta del servidor: {response}")
