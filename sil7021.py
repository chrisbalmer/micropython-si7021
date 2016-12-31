"""sil7021
"""
from time import sleep

class Sil7021(object):
    """Sil7021
    """

    SI7021_DEFAULT_ADDRESS = 0x40
    SI7021_MEASTEMP_NOHOLD_CMD = bytearray([0xF3])
    SI7021_MEASRH_NOHOLD_CMD = bytearray([0xF5])
    SI7021_RESET_CMD = bytearray([0xFE])


    def __init__(self, i2c, address=SI7021_DEFAULT_ADDRESS):
        self.i2c = i2c
        self.address = address


    def read_temperature(self):
        """temperature
        """
        temperature, verified = self._get_data(self.SI7021_MEASTEMP_NOHOLD_CMD)
        celcius = temperature * 175.72 / 65536 - 46.85
        fahrenheit = celcius * 1.8 + 32
        if verified:
            return {'celcius': celcius, 'fahrenheit': fahrenheit}
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
        value = data[0] << 8
        value = value | data[1]

        verified = self._verify_checksum(data)
        return (value, verified)


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
