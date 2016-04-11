import csv
import time

class Logging (object):
  def __init__(self,outfile):
    #self.freq = 0.1
    f = open(outfile,'wb')
    self.writer = csv.writer(f,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    self.writer.writerow(["TIME","TEMP","TARGET","PRESSURE"])

  def log(self,temp,target,pressure):
    self.writer.writerow(["%.5f" % time.time(),temp,target,pressure])

