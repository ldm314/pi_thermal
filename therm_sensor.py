from w1thermsensor import W1ThermSensor
class ThermSensor (object):
  def __init__(self):
    self.sensor = W1ThermSensor()

  def degrees_c(self):
    return self.sensor.get_temperature()
    
