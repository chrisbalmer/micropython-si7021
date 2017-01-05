'Quick example for the i2c driver.'

def run_example():
    '''Runs all of the methods from the i2c driver. Imports are included in the
    method for re-importing any updates when testing.

    '''
    import si7021
    import machine
    i2c = machine.I2C(machine.Pin(5), machine.Pin(4))

    temp_sensor = si7021.Si7021(i2c)
    print('Serial:              {value}'.format(value=temp_sensor.serial))
    print('Identifier:          {value}'.format(value=temp_sensor.identifier))
    print('Temperature:         {value}'.format(value=temp_sensor.temperature))
    print('Relative Humidity:   {value}'.format(
        value=temp_sensor.relative_humidity))

    temp_sensor.reset()
    print('\nModule reset.\n')

    print('Temperature:         {value}'.format(value=temp_sensor.temperature))
    print('Relative Humidity:   {value}'.format(
        value=temp_sensor.relative_humidity))

    print('Fahrenheit:          {value}'.format(
        value=si7021.convert_celcius_to_fahrenheit(temp_sensor.temperature)))
