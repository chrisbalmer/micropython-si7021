# Si7021 Library

This is a micropython driver written for the [Adafruit Si7021](https://www.adafruit.com/products/3251) breakout. The included example is designed to run on an Adafruit Feather Huzzah but can be easily modified for other controllers by changing the pins used.

Some parts based on the [Adafruit Si7021 C++ driver](https://github.com/adafruit/Adafruit_Si7021).

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

print(temp_sensor.temperature)
24.7722

print(temp_sensor.humidity)
38.59

temp_sensor.reset()

print(temp_sensor.temperature)
24.78291

print(temp_sensor.humidity)
37.8652

print(si7021.convert_celcius_to_fahrenheit(temp_sensor.temperature))
76.43548
```