#!/usr/bin/env python3
import asyncio
import logging
import uuid

from bleak import BleakScanner, BleakClient

# Enable debug output
# logging.basicConfig(level=logging.DEBUG)

DEVICE_NAME = "m5-stack"
SERVICE_UUID = uuid.UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
CHAR_UUID = uuid.UUID("beb5483e-36e1-4688-b7f5-ea07361b26a8")


async def run(loop):
    print("Searching devices...")
    devices = await BleakScanner.discover()

    device = list(filter(lambda d: d.name == DEVICE_NAME, devices))
    if len(device) == 0:
        raise RuntimeError(f"Failed to find a device name '{DEVICE_NAME}'")

    address = device[0].address
    print(f"Connecting to the device... (address: {address})")
    async with BleakClient(address, loop=loop) as client:
        print("Message from the device...")
        value = await client.read_gatt_char(CHAR_UUID)
        print(value.decode())

        print("Sending message to the device...")
        message = bytearray(b"hi!")
        await client.write_gatt_char(CHAR_UUID, message, True)

        def callback(sender, data):
            print(f"Received: {data}")

        print("Subscribing to characteristic changes...")
        await client.start_notify(CHAR_UUID, callback)

        print("Waiting 60 seconds to receive data from the device...")
        await asyncio.sleep(60)


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
