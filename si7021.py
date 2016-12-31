"""si7021
"""
from time import sleep

class Si7021(object):
    """Si7021
    """

    SI7021_DEFAULT_ADDRESS = 0x40
    SI7021_MEASTEMP_NOHOLD_CMD = bytearray([0xF3])
    SI7021_MEASRH_NOHOLD_CMD = bytearray([0xF5])
    SI7021_RESET_CMD = bytearray([0xFE])
    SI7021_ID1_CMD = bytearray([0xFA, 0x0F])
    SI7021_ID2_CMD = bytearray([0xFC, 0xC9])
    SI7021_ID_COMMANDS = [SI7021_ID1_CMD, SI7021_ID2_CMD]


    def __init__(self, i2c, address=SI7021_DEFAULT_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.serial, self.identifier = self._get_device_info()


    def read_temperature(self):
        """temperature
        """
        temperature, verified = self._get_data(self.SI7021_MEASTEMP_NOHOLD_CMD)
        celcius = temperature * 175.72 / 65536 - 46.85
        if verified:
            return celcius
        else:
            return None

    def read_temperature_as_fahrenheit(self):
        """temperature as fahrenheit
        """
        celcius = self.read_temperature()
        if celcius:
            return celcius * 1.8 + 32
        else:
            return None


    def read_humidity(self):
        """humidity
        """
        humidity, verified = self._get_data(self.SI7021_MEASRH_NOHOLD_CMD)
        humidity = humidity * 125 / 65536 - 6
        if verified:
            return humidity
        else:
            return None


    def reset(self):
        """Reset
        """
        self.i2c.writeto(self.address, self.SI7021_RESET_CMD)
        sleep(0.050)


    def _get_data(self, command):
        """get_data
        """
        data = bytearray(3)
        self.i2c.writeto(self.address, command)
        sleep(0.025)

        self.i2c.readfrom_into(self.address, data)
        value = self._convert_to_integer(data[:2])

        verified = self._verify_checksum(data)
        return (value, verified)


    def _get_device_info(self):
        # Serial 1st half
        self.i2c.writeto(self.address, self.SI7021_ID1_CMD)
        id1 = bytearray(8)
        sleep(0.025)
        self.i2c.readfrom_into(self.address, id1)

        # Serial 2nd half
        self.i2c.writeto(self.address, self.SI7021_ID2_CMD)
        id2 = bytearray(6)
        sleep(0.025)
        self.i2c.readfrom_into(self.address, id2)

        combined_id = bytearray([id1[0], id1[2], id1[4], id1[6],
                                 id2[0], id2[1], id2[3], id2[4]])

        serial = self._convert_to_integer(combined_id)
        identifier = self._get_device_identifier(id2[0])

        return serial, identifier

    def _convert_to_integer(self, bytes_to_convert):
        integer = None
        for chunk in bytes_to_convert:
            if not integer:
                integer = chunk
            else:
                integer = integer << 8
                integer = integer | chunk
        return integer


    def _get_device_identifier(self, identifier_byte):
        if identifier_byte == 0x00 or identifier_byte == 0xFF:
            return 'engineering sample'
        elif identifier_byte == 0x0D:
            return 'Si7013'
        elif identifier_byte == 0x14:
            return 'Si7020'
        elif identifier_byte == 0x15:
            return 'Si7021'
        else:
            return 'unknown'


    def _verify_checksum(self, data):
        """verify_checksum
        """
        crc = 0
        value = data[:2]
        checksum = int(data[2:3][0])
        for i in range(0, 2):
            crc = crc ^ value[i]
            for _ in range(8, 0, -1):
                if int(crc) & 0x80:
                    crc = (crc << 1) ^ 0x131
                else:
                    crc = (int(crc) << 1)
        if crc != checksum:
            return False
        else:
            return True
