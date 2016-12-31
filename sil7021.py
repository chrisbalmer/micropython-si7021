"""sil7021
"""
from time import sleep

class Sil7021(object):
    """Sil7021
    """

    SI7021_DEFAULT_ADDRESS = 0x40
    SI7021_MEASTEMP_NOHOLD_CMD = bytearray([0xF3])

    def __init__(self, i2c, address=SI7021_DEFAULT_ADDRESS):
        self.i2c = i2c
        self.address = address

    def temperature(self):
        """temperature
        """
        data = bytearray(3)
        self.i2c.writeto(self.address, self.SI7021_MEASTEMP_NOHOLD_CMD)
        sleep(0.025)

        self.i2c.readfrom_into(self.address, data)
        print(data)
        temperature = data[0] << 8
        temperature = temperature | data[1]
        celcius = temperature * 175.72 / 65536 - 46.85
        fahrenheit = celcius * 1.8 + 32
        print(celcius)
        print(fahrenheit)
        if self._verify_checksum(data):
            return {'celcius': celcius, 'fahrenheit': fahrenheit}
        else:
            return None

    def _verify_checksum(self, data):
        crc = 0
        value = data[:2]
        print(value)
        checksum = int(data[2:3][0])
        print(checksum)
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
