# Si7021 Library

This is a micropython driver written for the [Adafruit Si7021](https://www.adafruit.com/products/3251) breakout. The included example is designed to run on an Adafruit Feather Huzzah but can be easily modified for other controllers by changing the pins used.

## Requirements:

- MicroPython (tested on v1.8.6)
- [Adafruit Si7021](https://www.adafruit.com/products/3251)

## Example:

![Fritzing Diagram](example.png?raw=true "Fritzing Diagram")

```
import si7021
import machine
i2c = machine.I2C(machine.Pin(5), machine.Pin(4))

temp_sensor = si7021.Si7021(i2c)
print(temp_sensor.serial)
2883507688463925247

print(temp_sensor.identifier)
Si7021

print(temp_sensor.read_temperature())
19.09862

print(temp_sensor.read_temperature_as_fahrenheit())
66.3775

print(temp_sensor.read_humidity())
31.79221

temp_sensor.reset()

print(temp_sensor.read_temperature())
19.10933

print(temp_sensor.read_temperature_as_fahrenheit())
66.39676

print(temp_sensor.read_humidity())
31.76169
```