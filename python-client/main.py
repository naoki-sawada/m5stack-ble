import logging
import time
import uuid

import Adafruit_BluefruitLE


# Enable debug output.
#logging.basicConfig(level=logging.DEBUG)

SERVICE_UUID = uuid.UUID('4fafc201-1fb5-459e-8fcc-c5c9c331914b')
CHAR_UUID    = uuid.UUID('beb5483e-36e1-4688-b7f5-ea07361b26a8')


ble = Adafruit_BluefruitLE.get_provider()

def main():
    ble.clear_cached_data()

    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    print('Disconnecting any connected devices...')
    ble.disconnect_devices([SERVICE_UUID])

    # Scan devices.
    print('Searching device...')
    try:
        adapter.start_scan()

        #device = ble.find_device(service_uuids=[SERVICE_UUID])
        device = ble.find_device(name="m5-stack")
        if device is None:
            raise RuntimeError('Failed to find device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        print('Discovering services...')
        device.discover([SERVICE_UUID], [CHAR_UUID])

        # Find the service and its characteristics.
        uart = device.find_service(SERVICE_UUID)
        chara = uart.find_characteristic(CHAR_UUID)

        print('Message from device...')
        v = chara.read_value()
        print(v)

        # Write a string to the characteristic.
        print('Sending message to device...')
        chara.write_value(b'hi!')

        def received(data):
            print('Received: {0}'.format(data))

        # Turn on notification of characteristics using the callback above.
        print('Subscribing to characteristic changes...')
        chara.start_notify(received)

        # Now just wait for 30 seconds to receive data.
        print('Waiting 60 seconds to receive data from the device...')
        time.sleep(60)
    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
