import si7021
import machine
i2c = machine.I2C(machine.Pin(5), machine.Pin(4))

temp_sensor = si7021.Si7021(i2c)
temp_sensor._get_serial()

temp_sensor.read_temperature()
temp_sensor.read_humidity()


temp_sensor.reset()

temp_sensor.read_temperature()
temp_sensor.read_humidity()
