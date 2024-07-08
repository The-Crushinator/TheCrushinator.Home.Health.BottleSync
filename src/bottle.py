import asyncio
from bleak import BleakScanner, BleakClient, BLEDevice, BleakGATTServiceCollection, BleakGATTCharacteristic

class Bottle(BleakClient):
    """
    Class for interacting with the Hidrate Spark 3 water bottle. This is a wrapper around the BleakClient class.
    The intent is to provide a class that can be instantiated multiple times to handle multiple water bottles (untested).
    """

    _services: BleakGATTServiceCollection = None


    async def get_services(self, verbose: bool = False) -> BleakGATTServiceCollection:
        """
        Get the services and characteristics of the water bottle. This is a wrapper around the BleakClient.get_services() method.
        This function will cache the services response preventing multiple calls to the water bottle.
        """
        if self._services is None:
            self._services = await super().get_services()

        if verbose:
            for service in self._services:
                print("Service: {0}".format(service))
                for characteristic in service.characteristics:
                    print("  Characteristic: {0}".format(characteristic))

        return self._services

    async def _get_data_point(self, handle: int, verbose: bool = False) -> bytearray:
        """
        Gets a data point from the water bottle. This is used for reading a single register.

        :param services: The BleakGATTServiceCollection containing the services and characteristics
        :param handle: The integer handle of the characteristic to read (e.g. 23 for battery level)
        :param verbose: If True, print the value of the characteristic before returning
        :return: The value of the characteristic
        :rtype: bytearray
        """
        characteristic = (await self.get_services()).get_characteristic(handle)

        if 'read' not in characteristic.properties:
            print(f"Characteristic {handle} is not readable- properties are {characteristic.properties}")
            return None
        
        value = await self.read_gatt_char(characteristic)

        if verbose:
            print(f"Characteristic {handle} ({characteristic.description})::: Value: {value}")

        return value
    
    async def _set_data_point(self, handle: int, value: bytearray, verbose: bool = False) -> None:
        """
        Sets a data point on the water bottle. This is used for writing a single register.

        :param services: The BleakGATTServiceCollection containing the services and characteristics
        :param handle: The integer handle of the characteristic to write (e.g. 32 for LED control)
        :param value: The value to write to the characteristic
        :param verbose: If True, print the value written to the characteristic before returning
        """
        characteristic = (await self.get_services()).get_characteristic(handle)

        if 'write' not in characteristic.properties:
            print(f"Characteristic {handle} is not readable- properties are {characteristic.properties}")
            return None
        
        await self.write_gatt_char(characteristic, value)

        if verbose:
            print(f"Characteristic {handle} ({characteristic.description})::: Written value: {value}")

    @staticmethod
    def _get_size_from_byte_array(data: bytearray) -> int:
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
    
    @staticmethod
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
            d1 = Bottle.clamp(((sip_Start - min(sip_Start, sip_min)) / d2), 0.0, 1.0)
            d2 = Bottle.clamp(((sip_stop - min(sip_stop, sip_min)) / d2), 0.0, 1.0)
            sip_size = ((Bottle.correct_result(0, d1) - Bottle.correct_result(0, d2)) * bottle_size)

            print(f"sip_size: {sip_size}")
            print(f"sip_total: {sip_total}")
            print(f"sip_seconds_ago: {sip_seconds_ago}")
            print(f"sip_percentage?: {sip_percentage}")
            print(f"sip_min: {sip_min}")
            print(f"sip_max: {sip_max}")
        else:
            print(f"Value length not greater than 16: {len(data)}")
    
    async def get_battery_level_percentage(self) -> int:
        """
        Get the battery level percentage from the water bottle.

        :param services: The BleakGATTServiceCollection containing the services and characteristics
        :return: The battery level percentage
        :rtype: int
        """
        value = await self._get_data_point(23)
        value = int.from_bytes(value, byteorder='little')
        return value

    #region Getters
    async def get_model_number_string(self):
        """
        Get the model number string from the water bottle.
        """
        value = await self._get_data_point(36)
        return value

    async def get_manufacturer_name_string(self):
        """
        Get the manufacturer name string from the water bottle.
        """
        value = await self._get_data_point(38)
        return value

    async def get_serial_number_string(self):
        """
        Get the serial number string from the water bottle.
        """
        value = await self._get_data_point(40)
        return value

    async def get_firmware_revision_string(self):
        """
        Get the firmware revision string from the water bottle.
        """
        value = await self._get_data_point(42)
        return value

    async def get_hardware_revision_string(self):
        """
        Get the hardware revision string from the water bottle.
        """
        value = await self._get_data_point(44)
        return value

    async def get_software_revision_string(self):
        """
        Get the software revision string from the water bottle.
        """
        value = await self._get_data_point(46)
        return value
    
    async def get_bottle_size(self) -> int:
        """
        Get the size of the water bottle in milliliters.
        """
        appearance = await self._get_data_point(12, verbose=True)
        size = self._get_size_from_byte_array(appearance)
        return size

    async def get_next_sip(self):
        """
        Get the next sip value from the water bottle.
        Triggers multiple callback events as the bottle sends to the BLE client using the configured callback.
        """
        await self._set_data_point(49, bytearray([0x57]))
    #endregion

    #region Setters
    async def set_sip_led(self, enabled: bool):
        """
        Set the LED on the water bottle to indicate a sip was taken.
        """
        value = bytearray([0xB1]) if enabled else bytearray([0xB0])
        response = await self._set_data_point(32, value)
        return response
    #endregion

    #region Utils
    @staticmethod
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

    @staticmethod
    def correct_result(kind, value):
        """
        Correct the returned value based on the bottle kind. This is from characterisation of the bottle.
        """
        if kind == 0:
            return value
        elif kind == 1:
            return value
        else:
            return 0.0
    #endregion
    