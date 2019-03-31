from appJar import gui
import time
clockTime = 0
clockIsRunning = False

def startClock(btn):
    global clockIsRunning
    clockIsRunning = True
    runClock(clockIsRunning)

def runClock(runTime):
    global clockTime
    while runTime and clockTime <= 10:
        clockTime += 1
        app.setLabel("clock", clockTime)
        app.after(1000, runClock)

def updateClock(clockTime):
    app.queueFunction(app.setLabel, "clock", clockTime)

# create a GUI variable called app

app = gui("Test Clock")
app.setFont(18)

# add GUI elements : a label & a button
app.addLabel("clock", "The Time is 0")
app.addButton("Start Clock", startClock)

# put the updateMeter function in its own thread
app.thread(updateClock, clockTime)

# start the GUI
app.go()
