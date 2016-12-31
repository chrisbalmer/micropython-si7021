import sil7021
import machine
i2c = machine.I2C(machine.Pin(5), machine.Pin(4))

temp_sensor = sil7021.Sil7021(i2c)
temp_sensor.read_temperature()
temp_sensor.read_humidity()

temp_sensor.reset()

temp_sensor.read_temperature()
temp_sensor.read_humidity()
