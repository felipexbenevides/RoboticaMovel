from nxt.sensor.digital import BaseDigitalSensor


class TouchSensor(BaseDigitalSensor):
    I2C_ADDRESS = BaseDigitalSensor.I2C_ADDRESS.copy()
