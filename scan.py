import asyncio
from bleak import BleakScanner

async def main():
    # Print a message to the console
    print()
    print("Scanning for BLE devices...")
    print("  Timeout for devices to respond is 30 seconds")
    print("----------------------------------------------")

    # Discover BLE devices
    devices = await BleakScanner.discover(timeout=30)
    for device in devices:
        print(device)

asyncio.run(main())