import si7021
import machine
i2c = machine.I2C(machine.Pin(5), machine.Pin(4))

temp_sensor = si7021.Si7021(i2c)
print(temp_sensor.serial)
print(temp_sensor.identifier)
print(temp_sensor.temperature)
print(temp_sensor.humidity)

temp_sensor.reset()

print(temp_sensor.temperature)
print(temp_sensor.humidity)

print(si7021.convert_celcius_to_fahrenheit(temp_sensor.temperature))