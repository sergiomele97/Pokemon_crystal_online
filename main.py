import emulator
import server
import asyncio

server_connection = server.ServerConnection()
emulator = emulator.Emulator()

# Para cuando retome el proyecto:
# me gustaria implementar una window sdl2 con opcion para conectarse al servidor y logs de errores
# y opcion de jugar offline. Seria la pantalla de presentación de la aplicacion.

async def run_program():

    await asyncio.gather(emulator.run(), server_connection.connect())


if __name__ == "__main__":
    asyncio.run(run_program())
