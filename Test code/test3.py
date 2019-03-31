from appJar import gui
import time
percent_complete = 0

current_object = 0
def press(btn):
    global current_object
    current_object = 0
    processList()

def processList():
    global current_object
    objects = [1,3,6]
    total = len(objects)
    if current_object < total:
        i = objects[current_object]
        print(i)
        current_object += 1
        current_percent_complete = (current_object / total) * 100
        app.setMeter("progress", current_percent_complete)
        app.after(1000, processList)

def updateMeter(percent_complete):
    app.queueFunction(app.setMeter, "progress", percent_complete)

# create a GUI variable called app

app = gui("Login Window")
app.setBg("orange")
app.setFont(18)

# add GUI elements : a label, a meter, & a button

app.addLabel("title", "COUNTER")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "orange")

app.addMeter("progress")
app.setMeterFill("progress", "green")

app.addButton("START COUNTING", press)

# put the updateMeter function in its own thread

app.thread(updateMeter, percent_complete)

# start the GUI

app.go()
