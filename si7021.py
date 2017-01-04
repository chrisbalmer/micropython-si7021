'''This module implements a driver for the Si7021 humidity and temperature
sensor.

Datasheet:
https://www.silabs.com/Support%20Documents%2FTechnicalDocs%2FSi7021-A20.pdf

'''

from time import sleep

class CRCError(Exception):
    'Data failed a CRC check.'
    pass


class Si7021(object):
    'Driver for the Si7021 temperature sensor.'
    SI7021_DEFAULT_ADDRESS = 0x40
    SI7021_MEASTEMP_NOHOLD_CMD = bytearray([0xF3])
    SI7021_MEASRH_NOHOLD_CMD = bytearray([0xF5])
    SI7021_RESET_CMD = bytearray([0xFE])
    SI7021_ID1_CMD = bytearray([0xFA, 0x0F])
    SI7021_ID2_CMD = bytearray([0xFC, 0xC9])
    I2C_WAIT_TIME = 0.025


    def __init__(self, i2c, address=SI7021_DEFAULT_ADDRESS):
        'Initialize an Si7021 sensor object.'
        self.i2c = i2c
        self.address = address
        self.serial, self.identifier = self._get_device_info()


    @property
    def temperature(self):
        'Return the temperature in Celcius.'
        temperature = self._get_data(self.SI7021_MEASTEMP_NOHOLD_CMD)
        celcius = temperature * 175.72 / 65536 - 46.85
        return celcius


    @temperature.setter
    def temperature(self, value):
        raise AttributeError('can\'t set attribute')


    @property
    def humidity(self):
        'Return the humidity as a percentage. i.e. 35.59927'
        humidity = self._get_data(self.SI7021_MEASRH_NOHOLD_CMD)
        humidity = humidity * 125 / 65536 - 6
        return humidity


    @humidity.setter
    def humidity(self, value):
        raise AttributeError('can\'t set attribute')


    def reset(self):
        'Reset the sensor.'
        self.i2c.writeto(self.address, self.SI7021_RESET_CMD)
        sleep(self.I2C_WAIT_TIME)


    def _get_data(self, command):
        'Retrieve data from the sensor and verify it with a CRC check.'
        data = bytearray(3)
        self.i2c.writeto(self.address, command)
        sleep(self.I2C_WAIT_TIME)

        self.i2c.readfrom_into(self.address, data)
        value = self._convert_to_integer(data[:2])

        verified = self._verify_checksum(data)
        if not verified:
            raise CRCError('Data read off i2c bus failed CRC check.',
                           data[:2],
                           data[-1])
        return value


    def _get_device_info(self):
        '''Get the serial number and the sensor identifier. The identifier is
        part of the bytes returned for the serial number.

        '''
        # Serial 1st half
        self.i2c.writeto(self.address, self.SI7021_ID1_CMD)
        id1 = bytearray(8)
        sleep(self.I2C_WAIT_TIME)
        self.i2c.readfrom_into(self.address, id1)

        # Serial 2nd half
        self.i2c.writeto(self.address, self.SI7021_ID2_CMD)
        id2 = bytearray(6)
        sleep(self.I2C_WAIT_TIME)
        self.i2c.readfrom_into(self.address, id2)

        combined_id = bytearray([id1[0], id1[2], id1[4], id1[6],
                                 id2[0], id2[1], id2[3], id2[4]])

        serial = self._convert_to_integer(combined_id)
        identifier = self._get_device_identifier(id2[0])

        return serial, identifier

    def _convert_to_integer(self, bytes_to_convert):
        'Use bitwise operators to convert the bytes into integers.'
        integer = None
        for chunk in bytes_to_convert:
            if not integer:
                integer = chunk
            else:
                integer = integer << 8
                integer = integer | chunk
        return integer


    def _get_device_identifier(self, identifier_byte):
        '''Convert the identifier byte to a device identifier. Values are based
        on the information from page 24 of the datasheet.

        '''
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
        ''''Verify the checksum using the polynomial from page 19 of the
        datasheet.

        x8 + x5 + x4 + 1 = 0x131 = 0b100110001

        Valid Example:
        byte1: 0x67 [01100111]
        byte2: 0x8c [10001100]
        byte3: 0xfc [11111100] (CRC byte)

        '''
        crc = 0
        values = data[:2]
        checksum = int(data[-1])
        for value in values:
            crc = crc ^ value
            for _ in range(8, 0, -1):
                if crc & 0x80: #10000000
                    crc <<= 1
                    crc ^= 0x131 #100110001
                else:
                    crc <<= 1
        if crc != checksum:
            return False
        else:
            return True

def convert_celcius_to_fahrenheit(celcius):
    'Convert a Celcius measurement into a Fahrenheit measurement.'
    return celcius * 1.8 + 32
