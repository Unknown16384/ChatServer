import asyncio
from aioconsole import ainput

host = 'localhost'
port = 8888

async def main():
    reader, writer = await asyncio.open_connection(host, port)
    await asyncio.gather(chat_write(writer), chat_read(reader))
async def chat_read(reader):
    while True:
        text = await reader.readline()
        print(text.decode().strip())
async def chat_write(writer):
    while True:
        message = await ainput() + '\n'
        writer.write(message.encode())
        await writer.drain()
asyncio.run(main())