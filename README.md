# Si7021 Library

This is a micropython driver written for the [Adafruit Si7021](https://www.adafruit.com/products/3251) breakout. The included example is designed to run on an Adafruit Feather Huzzah but can be easily modified for other controllers by changing the pins used.

Some parts based on the [Adafruit Si7021 C++ driver](https://github.com/adafruit/Adafruit_Si7021).

## Requirements:

- MicroPython (tested on v1.8.6)
- [Adafruit Si7021](https://www.adafruit.com/products/3251)

## Example:

![Fritzing Diagram](example.png?raw=true "Fritzing Diagram")

```
>>> import example
>>> example.run_example()
Serial:              2883507688463925247
Identifier:          Si7021
Temperature:         21.88713
Relative Humidity:   30.55624

Module reset.

Temperature:         21.89787
Relative Humidity:   30.53336
Fahrenheit:          71.45477
>>> 
```