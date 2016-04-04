import RPi.GPIO as GPIO

PIN_CLK = 27
PIN_DO  = 22
PIN_CS  = 17
V_REF   = 4.9 

class ADC0831 (object):
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_DO,  GPIO.IN)
    GPIO.setup(PIN_CLK, GPIO.OUT)
    GPIO.setup(PIN_CS,  GPIO.OUT)

  # read SPI data from ADC8032
  def getADC(self):
    GPIO.output(PIN_CS, True)      # clear last transmission
    GPIO.output(PIN_CS, False)     # bring CS low
    GPIO.output(PIN_CLK, False)  # start clock low

    GPIO.output(PIN_CLK, True)  #one clock pulse before data
    GPIO.output(PIN_CLK, False)

    ad = 0
    for i in range(8):
      GPIO.output(PIN_CLK, True)
      GPIO.output(PIN_CLK, False)
      ad <<= 1 # shift bit
      if (GPIO.input(PIN_DO)):
        ad |= 0x1 # set first bit

    GPIO.output(PIN_CS, True)

    return ad

  def getVolts(self):
    ad = self.getADC()
    return round((ad / 255.0) * V_REF,3)

if __name__ == "__main__":
  import time
  import os

  s = ADC0831()

  while True:
    print "Volts: {}".format(s.getVolts())
    time.sleep(1)
