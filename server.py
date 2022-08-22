"""This file is responsible for establishing connection with client,
and responsibile for reading the data from client and executing commands"""
import asyncio
import signal
from services import Services
signal.signal(signal.SIGINT, signal.SIG_DFL)

async def execute_commands(reader,writer):
    """This function is responsible for writing data into client socket and reading data from client socket and executing the given commands."""
    address = writer.get_extra_info('peername')
    print(f"\n{address} is connected.")
    services_obj = Services()
    while True:
        inp = await reader.read(1000)
        data = inp.decode().strip()
        if data == "exit":
            break
        print(f"\nreceived {data} from {address}.")
        command_details = data.lstrip(" ").rstrip(" ").split(" ")
        command = command_details[0]
        if command in ("commands","COMMANDS"):
            writer.write(str(services_obj.commands()).encode())
        if command in ("register","REGISTER"):
            if len(command_details)==3:
                username = command_details[1]
                password = command_details[2]
                writer.write(str(services_obj.register(username,password)).encode())
            else:
                writer.write(str("Please enter command in below format\nregister <username> <password>").encode())
        if command in ("login","LOGIN"):
            if len(command_details)==3:
                username = command_details[1]
                password = command_details[2]
                writer.write(str(services_obj.login(username,password)).encode())
            else:
                writer.write(str("Please enter command in below format\nlogin <username> <password>").encode())
        if command in ("write_file","WRITE_FILE"):
            if len(command_details)==3:
                filename = command_details[1]
                content = command_details[2]
                writer.write(str(services_obj.write_file(filename,content)).encode())
            elif len(command_details)==2:
                filename = command_details[1]
                content = None
                writer.write(str(services_obj.write_file(filename,content)).encode())
            else:
                writer.write(str("Please enter command correctly.").encode())
        if command in ("read_file","READ_FILE"):
            if len(command_details)==2:
                filename = command_details[1]
                writer.write(str(services_obj.read_file(filename)).encode())
            else:
                writer.write(str("Please enter command in below format\nread_file <filename>.").encode())
        if command in ("create_folder","CREATE_FOLDER"):
            if len(command_details)==2:
                foldername = command_details[1]
                writer.write(str(services_obj.create_folder(foldername)).encode())
            else:
                writer.write(str("Please enter command in below format\ncreate_folder <name>.").encode())
        if command in ("change_folder","CHANGE_FOLDER"):
            if len(command_details)==2:
                foldername = command_details[1]
                writer.write(str(services_obj.change_folder(foldername)).encode())
            else:
                writer.write(str("Please enter command in below format\nchange_folder <name>.").encode())
        if command in ("list","LIST"):
            if len(command_details)==1:
                writer.write(str(services_obj.list_files()).encode())
            else:
                writer.write(str("Please enter command correctly.").encode())
        if command in ("quit","QUIT"):
            if len(command_details)==1:
                writer.write(str(services_obj.quit()).encode())
            else:
                writer.write(str("Please enter command correctly.").encode())
        if command not in ("register","REGISTER","login","LOGIN","change_folder","CHANGE_FOLDER","list","LIST","read_file","READ_FILE","create_folder","CREATE_FOLDER","write_file","WRITE_FILE","quit","QUIT"):
            writer.write(str("Command doesn't exist.").encode())
        await writer.drain()
    print("\nConnection closed.")
    writer.close()

async def main():
    """ This function initiates a server and establishes connection between server, client."""
    server = await asyncio.start_server(execute_commands,'127.0.0.1',8088)
    addr = server.sockets[0].getsockname()
    print(f"started on {addr}")
    async with server:
        await server.serve_forever()

asyncio.run(main())