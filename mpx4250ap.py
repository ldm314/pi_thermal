import adc0831

class MPX4250AP (object):
  def __init__(self):
    self.sensor = adc0831.ADC0831()

  def getKpa(self):
    val = self.sensor.getADC()
    return ((val/255.0) + 0.04)/0.004

if __name__ == "__main__":
  import time
  import os

  s = MPX4250AP()

  while True:
    print "kPa: {}".format(s.getKpa())
    time.sleep(1)

