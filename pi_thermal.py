from pids import Pid
import therm_sensor

#----------------------------------------------------------------------------

if __name__ == '__main__':

  import interpolations
  from threading import Thread

  def worm(terms, width=120):
    vals = []
    line = ' '*(width-2)
    for term in terms:
      left, x, right, sym = term
      h = int( interpolations.linear(left, right, x, 0, width-2) )
      line = line[:h] + sym + line[h+1:]
      vals.append(("%3.2f" % x).rjust(6))
    return "|" + line + "|"

  class Spinner ():
    def __init__(self):
      self.pos = 0;
      self.vals = ['|','/','-','\\']
    def next(self):
      self.pos += 1
      if self.pos >= len(self.vals):
        self.pos = 0
      return self.vals[self.pos]


  class ThermControl ():
    def __init__(self, **config):
      self.running = False
      self.maxwhere = 150.0
      self.minwhere = -10.0
      self.output = 0.0
      self.sensor = therm_sensor.ThermSensor()
      self.where = self.sensor.degrees_c()
      self.thread = False
    def set_output(self,val):
      self.output = val
    def measure(self):
      return self.where
    def run(self):
      while self.running:
        self.where = self.sensor.degrees_c()
    def start(self):
      self.running = True
      self.thread = Thread(target = self.run)
      self.thread.start()
    def stop(self):
      self.running = False
      self.thread.join()


  import math
  import random
  import time
  import curses

  screen = curses.initscr()
  curses.noecho()
  curses.cbreak()
  #curses.resizeterm(40,120)
  screen.nodelay(1)
  screen.keypad(True)


  #drawing area
  prompt = " Change Setpoint:\n\n Up/Down:     5.0\n Left/Right:  1.0 \n +/-:         0.1\n\n 'q' to quit.\n\n" 
  pad_x = 66 
  pad_y = 20

  pad = curses.newpad(pad_y,pad_x)
  pad.scrollok(True)

  string = ""
  spinner = Spinner()  
  therm = ThermControl()
  therm.start()

  pid = Pid()
  pid.range(-75.0, 75.0)
  pid.tune(.8,.3,.1)
  pid.set(0)

  start = time.time()

  try:
    while True:
      char = screen.getch()
      if char == ord('q'):
        break
      elif char == curses.KEY_RIGHT:
        pid.setpoint = pid.setpoint + 1.0
      elif char == curses.KEY_LEFT:
        pid.setpoint = pid.setpoint - 1.0
      elif char == curses.KEY_UP:
        pid.setpoint = pid.setpoint + 5.0
      elif char == curses.KEY_DOWN:
        pid.setpoint = pid.setpoint - 5.0
      elif char == ord('+'):
        pid.setpoint = pid.setpoint + 0.1
      elif char == ord('-'):
        pid.setpoint = pid.setpoint - 0.1


      pid.setpoint =  max(min(pid.setpoint, therm.maxwhere), therm.minwhere)     
      pid.set(pid.setpoint)

      stop = time.time()
      delta = stop-start

      pid.step(delta,therm.measure) #update pid loop
      therm.set_output(pid.output) #set to new target power

      disp = worm( [ (therm.minwhere, pid.setpoint, therm.maxwhere, '+'),
                     (therm.minwhere, therm.where, therm.maxwhere, '*')], pad_x)
      current = ("%3.2f" % therm.where).rjust(6)
      target = ("%3.2f" % pid.setpoint).rjust(6)
      minwhere = ("%3.2f" % therm.minwhere).rjust(6)
      maxwhere = ("%3.2f" % therm.maxwhere).rjust(6)
    
      string = "%s| Current Temp: %s, Target: %s, Min: %s, Max: %s |" % (spinner.next(),current,target,minwhere,maxwhere)
      screen.addstr(0,0,string)
      screen.addstr(1,0," " + '='*(len(string)-1))
      screen.addstr(1+pad_y,0," " + '='*(len(string)-1))
      screen.addstr(1+pad_y+1,0,prompt)
      screen.refresh()
      pad.addstr(disp)
      pad.refresh(0,0,2,1,pad_y,pad_x)
 
      time.sleep(0.1)
  finally:
    therm.stop()
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
