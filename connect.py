import asyncio
from bleak import BleakScanner, BleakClient, BLEDevice, BleakGATTServiceCollection, BleakGATTCharacteristic


# Service: 00001801-0000-1000-8000-00805f9b34fb (Handle: 1): Generic Attribute Profile
#   Characteristic: 00002a05-0000-1000-8000-00805f9b34fb (Handle: 2): Service Changed
#   Characteristic: 00002b29-0000-1000-8000-00805f9b34fb (Handle: 5): Client Supported Features
#   Characteristic: 00002b2a-0000-1000-8000-00805f9b34fb (Handle: 7): Database Hash
# Service: 00001800-0000-1000-8000-00805f9b34fb (Handle: 9): Generic Access Profile
#   Characteristic: 00002a00-0000-1000-8000-00805f9b34fb (Handle: 10): Device Name
#   Characteristic: 00002a01-0000-1000-8000-00805f9b34fb (Handle: 12): Appearance (Size??)
#   Characteristic: 00002a04-0000-1000-8000-00805f9b34fb (Handle: 14): Peripheral Preferred Connection Parameters
# Service: 22669e4c-2b42-2b98-4a43-80417170814f (Handle: 16): Unknown
#   Characteristic: 690c4427-bfe6-40a4-f349-d8f5bfa5d9a1 (Handle: 17): Unknown
#   Characteristic: 230c4427-bfe6-40a4-f349-d8f5bfa5d9a1 (Handle: 19): Unknown
# Service: 0000180f-0000-1000-8000-00805f9b34fb (Handle: 22): Battery Service
#   Characteristic: 00002a19-0000-1000-8000-00805f9b34fb (Handle: 23): Battery Level
# Service: 593f756e-fafc-49ba-8695-b39ca851b00b (Handle: 31): Unknown
#   Characteristic: e3578b0d-caa7-46d6-b7c2-7331c08de044 (Handle: 32): Unknown (Char Debug??? - Request next water sip with 0x57)
# Service: 0000180a-0000-1000-8000-00805f9b34fb (Handle: 35): Device Information
#   Characteristic: 00002a24-0000-1000-8000-00805f9b34fb (Handle: 36): Model Number String
#   Characteristic: 00002a29-0000-1000-8000-00805f9b34fb (Handle: 38): Manufacturer Name String
#   Characteristic: 00002a25-0000-1000-8000-00805f9b34fb (Handle: 40): Serial Number String
#   Characteristic: 00002a26-0000-1000-8000-00805f9b34fb (Handle: 42): Firmware Revision String
#   Characteristic: 00002a27-0000-1000-8000-00805f9b34fb (Handle: 44): Hardware Revision String
#   Characteristic: 00002a28-0000-1000-8000-00805f9b34fb (Handle: 46): Software Revision String
# Service: 45855422-6565-4cd7-a2a9-fe8af41b85e8 (Handle: 48): Unknown
#   Characteristic: 016e11b1-6c8a-4074-9e5a-076053f93784 (Handle: 49): Unknown (Number of sips available)
#   Characteristic: b44b03f0-b850-4090-86eb-72863fb3618d (Handle: 52): Unknown (SET_POINT ???)
#   Characteristic: 316c4914-1f59-462e-af06-185418674c0c (Handle: 55): Unknown
# Service: 4f817071-4180-434a-982b-422b4c9e6611 (Handle: 58): Unknown (LED Control Service)
#   Characteristic: a1d9a5bf-f5d8-49f3-a440-e6bf27440cb0 (Handle: 59): Unknown (LED_CONTROL)
#   Characteristic: b810e826-cf05-4b46-a725-07bc0fa2e5d9 (Handle: 62): Unknown (NORDIC_CUSTOM_COLOR / NORDIC_LED_CONTROL)
# Service: 75c276c3-8f97-20bc-a143-b354244886d4 (Handle: 65): Unknown
#   Characteristic: 6acf4f08-cc9d-d495-6b41-aa7e60c4e8a6 (Handle: 66): Unknown
#   Characteristic: d3d46a35-4394-e9aa-5a43-e7921120aaed (Handle: 68): Unknown
# Service: f65399a1-d953-472d-8ca9-1ac71c4ffcb8 (Handle: 71): Unknown
#   Characteristic: 1807a063-4e2d-4636-981a-35e93d1c7b94 (Handle: 72): Unknown
# Service: 0000181a-0000-1000-8000-00805f9b34fb (Handle: 75): Environmental Sensing
#   Characteristic: 00002a6e-0000-1000-8000-00805f9b34fb (Handle: 76): Temperature
# Service: 8d53dc1d-1db7-4cd3-868b-8a527460aa84 (Handle: 79): SMP Service
#   Characteristic: da2e7828-fbce-4e01-ae9e-261174997c48 (Handle: 80): SMP Characteristic


# Fields to consider / experiment with
# Add string constants for the UUIDs of the characteristics
ACKNOWLEDGE_DATA_POINT = '' # ???
ANDROID_SYNC_TIMES = 'e3578b0d-caa7-46d6-b7c2-7331c08de044' # GenericBTLEDevice
CLEAR = '6ac24e8b-056c-4077-8221-8f816ade71e6' # GenericBTLEDevice
READY_FOR_HISTORY = '016e11b1-6c8a-4074-9e5a-076053f93784' # GenericBTLEDevice
READY_FOR_HISTORY_FAST = '' # ???
#.field public static final BATTERY:Ljava/lang/String; = "00002a19-0000-1000-8000-00805f9b34fb"
BATTERY = '00002a19-0000-1000-8000-00805f9b34fb'
#.field public static final FIRMWARE_VERSION:Ljava/lang/String; = "00002a26-0000-1000-8000-00805f9b34fb"
FIRMWARE_VERSION = '00002a26-0000-1000-8000-00805f9b34fb'
#.field public static final H2O_TOTAL:Ljava/lang/String; = "6ac24e8b-056c-4077-8221-8f816ade71e6"
H2O_TOTAL = '6ac24e8b-056c-4077-8221-8f816ade71e6'
#.field public static final BOOTLOADER:Ljava/lang/String; = "00060001-f8ce-11e4-abf4-0002a5d5c51b"
BOOTLOADER = '00060001-f8ce-11e4-abf4-0002a5d5c51b'
#.field public static final CONFIG:Ljava/lang/String; = "31FB5B6C-0166-4C97-BA1D-BF0A82FBBCB6"
CONFIG = '31FB5B6C-0166-4C97-BA1D-BF0A82FBBCB6'
#.field public static final DATA_POINT:Ljava/lang/String; = "016e11b1-6c8a-4074-9e5a-076053f93784"
DATA_POINT = '016e11b1-6c8a-4074-9e5a-076053f93784'
#.field public static final DEBUG:Ljava/lang/String; = "e3578b0d-caa7-46d6-b7c2-7331c08de044"
DEBUG = 'e3578b0d-caa7-46d6-b7c2-7331c08de044'
#.field public static final LED_CONTROL:Ljava/lang/String; = "a1d9a5bf-f5d8-49f3-a440-e6bf27440cb0"
LED_CONTROL = 'a1d9a5bf-f5d8-49f3-a440-e6bf27440cb0'
#.field public static final NORDIC_CUSTOM_COLOR:Ljava/lang/String; = "B810E826-CF05-4B46-A725-07BC0FA2E5D9"
NORDIC_CUSTOM_COLOR = 'B810E826-CF05-4B46-A725-07BC0FA2E5D9'
#.field public static final NORDIC_LED_CONTROL:Ljava/lang/String; = "B810E826-CF05-4B46-A725-07BC0FA2E5D9"
NORDIC_LED_CONTROL = 'B810E826-CF05-4B46-A725-07BC0FA2E5D9'
#.field public static final SET_POINT:Ljava/lang/String; = "b44b03f0-b850-4090-86eb-72863fb3618d"
SET_POINT = 'b44b03f0-b850-4090-86eb-72863fb3618d'


# MAJOR VARIABLES (To be refactored in to class variables)
BOTTLE_SIZE = 0
SIP_WAITING = True

# callback for disconnecting
def callback(sender, **kwargs):
    print("Disconnected")
    print(sender)
    print(kwargs)

# Function to scan for devices
async def scan(timeout: int = 5) -> BLEDevice:
    # Print a message to the console
    print()
    print(f"Scanning for BLE devices (timeout {timeout} seconds)")
    print("----------------------------------------------")

    # Discover BLE devices
    devices = await BleakScanner.discover(timeout=5)
    for device in devices:
        # Print device name, just so we know
        print(device)
        # If the device name contains "h2o" (and name isn't none), return it
        if device.name is not None and "h2o" in device.name.lower():
            return device

async def get_services(client: BleakClient, verbose: bool = False) -> BleakGATTServiceCollection:
    services = await client.get_services()
    if verbose:
        for service in services:
            print("Service: {0}".format(service))
            for characteristic in service.characteristics:
                print("  Characteristic: {0}".format(characteristic))

    return services

async def get_data_point(client: BleakClient, services: BleakGATTServiceCollection, handle: int, verbose: bool = False) -> bytearray:
    """
    Gets a data point from the water bottle. This is used for reading a single register.

    :param client: The BleakClient- BLE client to use
    :param services: The BleakGATTServiceCollection containing the services and characteristics
    :param handle: The integer handle of the characteristic to read (e.g. 23 for battery level)
    :param verbose: If True, print the value of the characteristic before returning
    :return: The value of the characteristic
    :rtype: bytearray
    """
    characteristic = services.get_characteristic(handle)

    if 'read' not in characteristic.properties:
        print(f"Characteristic {handle} is not readable- properties are {characteristic.properties}")
        return None
    
    value = await client.read_gatt_char(characteristic)

    if verbose:
        print(f"Characteristic {handle} ({characteristic.description})::: Value: {value}")

    return value

async def set_data_point(client: BleakClient, services: BleakGATTServiceCollection, handle: int, value: bytearray, verbose: bool = False) -> None:
    """
    Sets a data point on the water bottle. This is used for writing a single register.

    :param client: The BleakClient- BLE client to use
    :param services: The BleakGATTServiceCollection containing the services and characteristics
    :param handle: The integer handle of the characteristic to write (e.g. 32 for LED control)
    :param value: The value to write to the characteristic
    :param verbose: If True, print the value written to the characteristic before returning
    """
    characteristic = services.get_characteristic(handle)

    if 'write' not in characteristic.properties:
        print(f"Characteristic {handle} is not readable- properties are {characteristic.properties}")
        return None
    
    await client.write_gatt_char(characteristic, value)

    if verbose:
        print(f"Characteristic {handle} ({characteristic.description})::: Written value: {value}")

def get_size_from_byte_array(data: bytearray) -> int:
    """
    Get the bottle size value from a byte array. The size is stored in bytes 0 and 1 of the array.

    :param data: The byte array to extract the size from
    :return: The size of the bottle
    :rtype: int
    """
    if len(data) < 2:
        return 0
    
    value = int.from_bytes(data[0:2], byteorder='little')

    return value

async def get_battery_level_percentage(client: BleakClient, services: BleakGATTServiceCollection):
    """
    Get the battery level percentage from the water bottle.

    :param client: The BleakClient- BLE client to use
    :param services: The BleakGATTServiceCollection containing the services and characteristics
    :return: The battery level percentage
    :rtype: int
    """
    value = await get_data_point(client, services, 23)
    value = int.from_bytes(value, byteorder='little')
    return value

async def get_model_number_string(client: BleakClient, services: BleakGATTServiceCollection):
    value = await get_data_point(client, services, 36)
    return value

async def get_manufacturer_name_string(client: BleakClient, services: BleakGATTServiceCollection):
    value = await get_data_point(client, services, 38)
    return value

async def get_serial_number_string(client: BleakClient, services: BleakGATTServiceCollection):
    value = await get_data_point(client, services, 40)
    return value

async def get_firmware_revision_string(client: BleakClient, services: BleakGATTServiceCollection):
    value = await get_data_point(client, services, 42)
    return value

async def get_hardware_revision_string(client: BleakClient, services: BleakGATTServiceCollection):
    value = await get_data_point(client, services, 44)
    return value

async def get_software_revision_string(client: BleakClient, services: BleakGATTServiceCollection):
    value = await get_data_point(client, services, 46)
    return value

async def set_sip_led(client: BleakClient, services: BleakGATTServiceCollection, enabled: bool):
    value = bytearray([0xB1]) if enabled else bytearray([0xB0])
    response = await set_data_point(client, services, 32, value)
    return response

async def get_bottle_size(client: BleakClient, services: BleakGATTServiceCollection) -> int:
    appearance = await get_data_point(client, services, 12, verbose=True)
    size = get_size_from_byte_array(appearance)
    return size

async def get_next_sip(client: BleakClient, services: BleakGATTServiceCollection):
    await set_data_point(client, services, 49, bytearray([0x57]))

def clamp(n, min, max):
    """
    Clamp a number to a range.

    :param n: The number to clamp
    :param min: The minimum value of the range
    :param max: The maximum value of the range
    """
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

def correctFraction(kind, value):
    if kind == 0:
        return value
    elif kind == 1:
        return value
    else:
        return 0.0


def parse_sip(data: bytearray, bottle_size: int = 1) -> int:
    """
    Parse the data from a sip notification. This will return the sip size, total sips, and other information.

    :param data: The data payload of the sip notification
    :param bottle_size: The size of the bottle
    :return: The size of the sip
    :rtype: int
    """
    if len(data) >= 16:
        sips_remaining = data[0]
        sip_percentage = data[1]
        sip_total = int.from_bytes(data[2:4], byteorder='little')
        sip_seconds_ago = int.from_bytes(data[4:8], byteorder='little')
        sip_min = int.from_bytes(data[8:10], byteorder='little')
        sip_max = int.from_bytes(data[10:12], byteorder='little')
        sip_Start = int.from_bytes(data[12:14], byteorder='little')
        sip_stop = int.from_bytes(data[14:16], byteorder='little')
        d2 = sip_max - min(sip_Start, sip_min)
        d1 = clamp(((sip_Start - min(sip_Start, sip_min)) / d2), 0.0, 1.0)
        d2 = clamp(((sip_stop - min(sip_stop, sip_min)) / d2), 0.0, 1.0)
        sip_size = ((correctFraction(0, d1) - correctFraction(0, d2)) * bottle_size)

        print(f"sip_size: {sip_size}")
        print(f"sip_total: {sip_total}")
        print(f"sip_seconds_ago: {sip_seconds_ago}")
        print(f"sip_percentage?: {sip_percentage}")
        print(f"sip_min: {sip_min}")
        print(f"sip_max: {sip_max}")
    else:
        print(f"Value length not greater than 16: {len(data)}")

async def handle_sip_notification(sender: BleakGATTCharacteristic, data: bytearray):
    """
    Handle a notification from the sip characteristic.
    This notification will have a data payload that holds either
    - the number of sips, or
    - the next sip data

    :param sender: The characteristic sender of the notification
    :param data: The data payload of the notification
    """
    # print(f"{sender}: {data}")
    if len(data) > 0:
        if data[0] > 0 and int.from_bytes(data[1:], byteorder='little') > 0:
            parse_sip(data, BOTTLE_SIZE)
        elif data[0] > 0:
            num_sips = data[0]
            print(f"Empty payload, number of sips remaining to read: {num_sips}")
            global SIP_WAITING
            SIP_WAITING = True
        else:
            print("No sip data available to read")


# Function to connect to a device
async def connect(device: BLEDevice | str):
    # Check if device is None
    if device is None:
        print("No device found")
        return
    
    print("Connecting to device...")
    # Connect to the device (using a context manager)
    async with BleakClient(device, timeout=30) as client:
        # Confirm the client is connected
        print("Connected: {0}".format(client.is_connected))

        # Collect services, List available services
        services = await get_services(client, verbose=False)
        
        # Read battery level from known service
        print("Battery: {0}%".format(await get_battery_level_percentage(client, services)))
        # Read model number string from known service
        print("Model Number: {0}".format(await get_model_number_string(client, services)))
        # Read manufacturer name string from known service
        print("Manufacturer Name: {0}".format(await get_manufacturer_name_string(client, services)))
        # Read serial number string from known service
        print("Serial Number: {0}".format(await get_serial_number_string(client, services)))
        # Read firmware revision string from known service
        print("Firmware Revision: {0}".format(await get_firmware_revision_string(client, services)))
        # Read hardware revision string from known service
        print("Hardware Revision: {0}".format(await get_hardware_revision_string(client, services)))
        # Read software revision string from known service
        print("Software Revision: {0}".format(await get_software_revision_string(client, services)))

        # Ensure sip LED is on
        await set_sip_led(client, services, True)

        global BOTTLE_SIZE
        BOTTLE_SIZE = await get_bottle_size(client, services)

        # # Advertise successful connection with LED pulses
        # value = await client.write_gatt_char(LED_CONTROL, bytearray([0x34]))
        # print("LED Control: {0}".format(value))

        i = 1

        # Start notifications for the data point characteristic (sips)
        await client.start_notify(services.get_characteristic(49), handle_sip_notification)
        
        # Start the read loop
        sleep_time = 5
        update_sip_time = 600 # 10 minutes
        count = 0
        global SIP_WAITING
        try:
            while True:
                await asyncio.sleep(sleep_time)
                count += 1

                if SIP_WAITING or (count * sleep_time) % update_sip_time == 0:
                    await client.write_gatt_char(services.get_characteristic(49), bytearray([0x57]))
                    SIP_WAITING = False
                    count = 0

        except asyncio.CancelledError:
            pass

        # Stop notifications for the data point characteristic (sips)
        await client.stop_notify(services.get_characteristic(49))

        
        # Make bottle glow
        # value = await client.read_gatt_char(NORDIC_LED_CONTROL)
        # print("Nordic LED Control: {0}".format(value))
        # value = await client.write_gatt_char(NORDIC_LED_CONTROL, bytearray([0xFF, 0xAA, 0x44, 0xCC]))
        # print("Nordic LED Control: {0}".format(value))
        
        # Tested: Doesn't work
        #value = await client.read_gatt_char(H2O_TOTAL)
        #print("H2O Total: {0}".format(value))



# Main function
async def main():
    # Scan for devices 5 times
    for _ in range(10):
        device = await scan()
        if device is not None:
            break
    #(Testing, use "F9:B8:E7:DC:C6:B0: h2oD9951")
    await connect(device)

if __name__ == "__main__":
    asyncio.run(main())
