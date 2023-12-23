import argparse
import json

DEVICE_NAME = "DEVICE_NAME"


def set_device_name(name: str):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump({DEVICE_NAME: name}, f)
    print(f'Current adb device: {get_device_name()}')


def get_device_name() -> str:
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config.get(DEVICE_NAME)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("deviceName", help="Example: localhost:00000 or emulator-5554", type=str)
    parser.add_argument("os", help="13", type=int)
    args = parser.parse_args()
    arg_device = args.deviceName
    arg_os = args.os
    set_device_name(f'{arg_device} ({arg_os})')
