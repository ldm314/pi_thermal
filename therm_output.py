import RPi.GPIO as GPIO

class ThermOutput (object):
  def __init__(self):
    #self.freq = 0.1  
    self.freq = 0.15  
    self.percent = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
    self.pwm = GPIO.PWM(18,self.freq)

  def start(self):
    self.pwm.start(self.percent)    

  def stop(self):
    self.pwm.stop()

  def set(self,percent):
    self.percent = percent
    self.pwm.ChangeDutyCycle(percent)
    
