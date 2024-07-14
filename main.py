import emulator
import server
import asyncio

server_connection = server.ServerConnection()
emulator = emulator.Emulator()


async def run_program():

    await asyncio.gather(emulator.run(), server_connection.connect())



if __name__ == "__main__":
    asyncio.run(run_program())
