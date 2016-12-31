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


    def _get_model_info(self):
        info = []

        # Serial 1st half
        self.i2c.writeto(self.address, self.SI7021_ID1_CMD)
        id1 = bytearray(8)
        sleep(0.025)
        self.i2c.readfrom_into(self.address, id1)
        print(id1)
        serial = id1[0] << 8
        serial = serial | id1[2]
        serial = serial << 8
        serial = serial | id1[4]
        serial = serial << 8
        serial = serial | id1[6]
        info.append(serial)

        sleep(0.025)

        # Serial 2nd half
        self.i2c.writeto(self.address, self.SI7021_ID2_CMD)
        id2 = bytearray(6)
        sleep(0.025)
        self.i2c.readfrom_into(self.address, id2)
        print(id2)
        serial = id2[0] << 8
        serial = serial | id2[1]
        serial = serial << 8
        serial = serial | id2[3]
        serial = serial << 8
        serial = serial | id2[4]
        info.append(serial)

        if id2[0] == 0x00 or id2[0] == 0xFF:
            model = 'engineering sample'
        elif id2[0] == 0x0D:
            model = 'Si7013'
        elif id2[0] == 0x14:
            model = 'Si7020'
        elif id2[0] == 0x15:
            model = 'Si7021'
        else:
            model = 'unknown'

        info.append(model)

        return info

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
