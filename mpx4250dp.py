import adc0831

class MPX4250DP (object):
  def __init__(self):
    self.sensor = adc0831.ADC0831()

  def getKpa(self):
    val = self.sensor.getVolts()
    offset = 0.192
    return ((val - offset))/0.00369

if __name__ == "__main__":
  import time
  import os

  s = MPX4250DP()

  while True:
    print "kPa: {}".format(s.getKpa())
    time.sleep(1)

