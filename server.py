import asyncio, logging, datetime

logging.basicConfig(level=logging.INFO, filename='chat.log',filemode='w', format='%(asctime)s %(message)s')
clients = {}
host = 'localhost'
port = 8888

async def main():
    server = await asyncio.start_server(handler, host, port)
    logging.info(f'Serving on {server.sockets[0].getsockname()}')
    async with server: await server.serve_forever()
async def handler(reader, writer):
    async def message(msg):
        writer.write((msg + '\n').encode())
        await writer.drain()
    global clients
    name = None
    await message('Enter your name:')
    while True:
        data = await reader.readline()
        if not data: break
        text = data.decode().strip()
        if name: await message_for_all(f'{name}: {text}')
        else:
            if text in clients: await message('Name is already in use.')
            else:
                name = text
                clients[name] = writer
                await message_for_all(f'{name} joined.')
    if name:
        del clients[name]
        await message_for_all(f'{name} has left.')
    writer.close()
    await writer.wait_closed()
async def message_for_all(msg):
    logging.info(msg)
    msg = datetime.datetime.now().strftime('[%H:%M:%S] ') + msg
    print(msg)
    for _, client in clients.items():
        client.write((msg + '\n').encode())
        await client.drain()

asyncio.run(main())