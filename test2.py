from time import sleep
from appJar import gui
clockTime = 0
start = False

def startClock(btn):
    global start
    start = True
    runClock(start)

def stopClock(btn):
    global start
    start = False

def runClock(status):
    global clockTime
    while status:
        clockTime += 1
        Date.setLabel("lb1", "Time = " + str(clockTime))
        sleep(1)
        global start
        status = start

Date = gui("Date")

Date.addLabel("lb1", "Time = 0")
Date.addButton("Play", startClock)
Date.addButton("Pause", stopClock)

Date.go()
