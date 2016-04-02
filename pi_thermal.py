from pids import Pid
import therm_sensor

#----------------------------------------------------------------------------

if __name__ == '__main__':

  import interpolations

  def worm(terms, width=120):
    vals = []
    line = ' '*width
    for term in terms:
      left, x, right, sym = term
      h = int( interpolations.linear(left, right, x, 0, width-2) )
      line = line[:h] + sym + line[h+1:]
      vals.append(("%3.2f" % x).rjust(6))
    print ":".join(vals) + "|" + line + "|"

  class ThermPid ():
    def __init__(self, **config):
      self.where = 25.0
      self.maxwhere = 150.0
      self.minwhere = -150.0
      self.output = 0.0
      #self.sensor = therm_sensor.ThermSensor()
    def set_output(self,val):
      self.output = val
    def measure(self):
      #insert read here
      # return self.sensor.degrees_c()
      self.where += self.output / 5.0
      self.where = max(min(self.where, self.maxwhere), self.minwhere)
      return self.where

  import math
  import random
  import time

  therm = ThermPid()
  pid = Pid()
  pid.range(-75.0, 75.0)
  pid.tune(.8,.3,.1)
  pid.set(0)
  for i in range(200):
      time.sleep(0.05)
      pid.step(0.05,therm.measure)
      therm.set_output(pid.output)
      #worm(pid.minout, pid.get(), pid.maxout)
      worm( [ (therm.minwhere, pid.setpoint, therm.maxwhere, '+'),
              (therm.minwhere, therm.where, therm.maxwhere, '*')] )
#      worm( [ (therm.minwhere, pid.setpoint, therm.maxwhere, '+'),
#              (therm.minwhere, therm.where, therm.maxwhere, '*'),
#	      (-75.0,pid.output,75.0, '#')] )
      if i % 20 == 9:
          pid.set(random.random() * 100 - 50)

