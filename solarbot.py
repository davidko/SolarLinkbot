#!/usr/bin/env/python
from barobo.linkbot import *
import time
import pylab

class SolarBot(Linkbot):
  def __init__(self):
    Linkbot.__init__(self)
    pylab.ion()
    pylab.hold(False)

  def getSolarData(self):
    value = self.getBreakoutADC(0)
    return value

  def _newton(self):
    pos = []
    data = []
    self.moveJoint(1, -15)
    self.moveJointNB(1, 30)
    while self.isMoving():
      pos.append(self.getJointAngle(1))
      print pos[-1]
      data.append(self.getSolarData())
    pylab.plot(pos, data)
    pylab.draw()
    index = data.index(min(data))
    self.moveJointTo(1, pos[index])
    x = pos[index]
    pos = []
    data = []
    self.moveJoint(2, -15)
    self.moveJointNB(2, 30)
    while self.isMoving():
      pos.append(self.getJointAngle(2))
      print pos[-1]
      data.append(self.getSolarData())
    pylab.plot(pos, data)
    pylab.draw()
    index = data.index(min(data))
    self.moveJointTo(2, pos[index])
    return (x, pos[index])

  def newton(self):
    [last_x, last_y, _] = self.getJointAngles()
    mag = 10
    while mag > 3:
      try:
        (x, y) = self._newton()
      except RuntimeError:
        print "Comms error... Continuing..."
        time.sleep(1)
        continue
      mag = math.sqrt( (last_x-x)**2 + (last_y-y)**2)
      last_x = x
      last_y = y

if __name__ == "__main__":
  bot = SolarBot()
  bot.connect()
  bot.setJointSpeed(1, 45/4.0) 
  bot.setJointSpeed(2, 45/4.0) 
  bot.newton()
  exit()
  bot.moveJointTo(1, -45)
  bot.moveJointToNB(1, 45)
  pos = []
  data = []
  starttime = time.time()
  while starttime > time.time() - 5.0:
    pos.append(bot.getJointAngle(1))
    data.append(bot.getSolarData())
    pylab.plot(pos, data)
    pylab.draw()
