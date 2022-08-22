"""This file is responsible for establishing connection with server,
and for passing commands given by user to server."""
import asyncio
async def connect_client():
    """This file is responsible for establishing connection for client with server."""
    reader,writer = await asyncio.open_connection("127.0.0.1",8088)
    data = ""
    while True:
        data = input("Enter command : ")
        if data == "":
            print("Command shouldn't be empty")
            continue
        writer.write(data.encode())
        inp = await reader.read(1000)
        message = str(inp.decode())
        print(message)
        if data == "quit" or data == "exit":
            break
    print("Connection closed")
    writer.close()
asyncio.run(connect_client())
