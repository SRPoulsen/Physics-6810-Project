from appJar import gui

class Game:
    def __init__(self):

        # get name and other student info from GUI. pass to student constructor
        # save our newly created student
        #self.mainStudent = Student(self.gui.getStudentName())
        self.student = Student()
        self.gui = GuiFormatter(Clock(self.processTick), self.student)

        self.gui.ready()

    def processTick(self, day, hour):  #Main method: Processes all functions that need to update every hour
        self.student.expTick()
        self.student.stressTick()
        self.gui.updateHUD(day, hour, self.student)


class Clock:
    WEEK_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    def __init__(self, act):
        self.clockDay = 0
        self.clockHour = 0             #Start at hour = 0
        self.clockIsRunning = False    #Start with the clock paused
        self.clockSpeed = 1000         #1000 ms delay on clock (1 s)
        self.action = act              #Passes in the action that should be performed every loop of runClock
        self.dateUnlocked = True

    def startClock(self):          #Changes the status to "clock is running"
        if not self.clockIsRunning:             #Makes sure the clock wasn't already running
            self.clockIsRunning = True

    def stopClock(self):           #Changes the status to "clock isn't running"
        self.clockIsRunning = False

    def runClock(self):            #action = processTick in Game class
        if self.clockIsRunning and self.dateUnlocked:       #Makes sure the clock is running and the date is unlocked
            self.clockHour += 1                             #Adds one hour to the clock
            if self.clockHour >= 24:
                self.clockHour -= 24
                self.clockDay += 1
            self.action(self.clockDay, self.clockHour)

    def speedS(self):              #Slowest speed (1 hour per second)
        self.clockSpeed = 1000

    def speedM(self):              #Middle speed
        self.clockSpeed = 500

    def speedF(self):              #Fasted speed
        self.clockSpeed = 250


class GuiFormatter:
    created = False                             #There has never been a created GUI before

    #Groups of buttons where only one button from each group is allowed to be active
    speedGroup = ['Slow', 'Medium', 'Fast']
    timeGroup = ['Play', 'Pause']
    actionGroup = ['Study', 'Relax', 'Sleep']

    def __init__(self, clk, ss):
        if GuiFormatter.created:            #Only allows one GUI to be created
            raise Exception('Instance already exists')

        GuiFormatter.created = True          #There has now been a created GUI
        self.clock = clk                     #Save the instance of the clock
        self.student = ss                    #Save the instance of the student

        #Calls on functions (below) to create and format the gui, as well as subWindows
        self.createAndFormatGui()
        self.createDateTimeDisplay()
        self.createStatusIndicators()
        self.createGuiButtons()
        self.initializeSubWindow("Carmen", "This is a test of the carmen app")
        self.initializeSubWindow("ReportCard", "This is a test of the report card")

        #Initialize the clock to run at "slow" speed, then begin looping through runClock
        self.app.setPollTime(self.clock.clockSpeed)
        self.app.registerEvent(self.clock.runClock)

        #Prompt user for their name, passes name to student
        self.student.name = self.getStudentName()

    #GUI formatting and initialization functions

    def createAndFormatGui(self):              #Creates and formats the main gui
        self.app = gui("Control Window")
        self.app.setSize(800,500)

    def createDateTimeDisplay(self):           #Creates the Date and Time display on gui
        self.app.addLabel("PauseLabel", "Paused", 0, 0)
        self.app.setLabelFg("PauseLabel", "red")
        self.app.addLabel("lb1", "Day: 0\tHour: 0", 0, 1)
        self.app.addLabel("DayOfWeek", "Sunday", 0, 2)

    def createGuiButtons(self):                #Creates all the buttons for gui
        self.app.addButton("Study", self.studyButton, 3, 0)
        self.app.addButton("Relax", self.relaxButton, 3, 1)
        self.app.addButton("Sleep", self.sleepButton, 3, 2)
        self.app.setButtonFg("Sleep", "Green")
        self.app.addButton("Play", self.playButton, 4, 0)
        self.app.addButton("Pause", self.pauseButton, 4, 1)
        self.app.addButton("Save", self.saveGame, 4, 2)
        self.app.addButton("Slow", self.slowButton, 5, 0)
        self.app.addButton("Medium", self.medButton, 5, 1)
        self.app.addButton("Fast", self.fastButton, 5, 2)
        self.app.setButtonFg("Slow", "Green")
        self.app.addButton("See Grades", self.gradesButton, 6, 0)
        self.app.addButton("See Report Card", self.reportCardButton, 6, 1)

    def createStatusIndicators(self):          #Creates the meters and labels that tell the players their stats on gui
        self.app.addLabel("expLabel", "Experience (Level 1)", 1, 0, 1)
        self.app.addLabel("strLabel", "Stress", 2, 0, 1)
        self.app.addMeter("Experience", 1, 1, 2)
        self.app.setMeterFill("Experience", "Green")
        self.app.addMeter("Stress", 2, 1, 2)
        self.app.setMeterFill("Stress", "Red")

    def initializeSubWindow(self, label, text):    #Creates a subWindow then immediatly hides it
        self.app.startSubWindow(label, modal = False)
        self.app.addMessage(label + "Label", text)
        self.app.stopSubWindow()

    #Button functions

    def playButton(self, btn):                 #When the "Play" button is pressed, start the clock
        self.app.setLabel("PauseLabel", " ")
        self.changeActiveButton("Play", GuiFormatter.timeGroup)
        self.clock.startClock()

    def pauseButton(self, btn):                #When the "Pause" button is pressed, stop the clock
        self.app.setLabel("PauseLabel", "Paused")
        self.changeActiveButton("Pause", GuiFormatter.timeGroup)
        self.clock.stopClock()

    def studyButton(self, btn):                #Changes studying to true, changes relax/sleep to false
        self.changeActiveAction('studying')
        self.changeActiveButton("Study", GuiFormatter.actionGroup)

    def relaxButton(self, btn):                #Changes relaxing to true, changes study/sleep to false
        self.changeActiveAction('relaxing')
        self.changeActiveButton("Relax", GuiFormatter.actionGroup)

    def sleepButton(self, btn):                #Changes sleeping to true, changes study/relax to false
        self.changeActiveAction('sleeping')
        self.changeActiveButton("Sleep", GuiFormatter.actionGroup)

    def slowButton(self):                      #Changes the clock speed to slow
        self.changeActiveButton("Slow", GuiFormatter.speedGroup)
        self.clock.speedS()
        self.app.setPollTime(self.clock.clockSpeed)

    def medButton(self):                       #Changes the clock speed to medium
        self.changeActiveButton("Medium", GuiFormatter.speedGroup)
        self.clock.speedM()
        self.app.setPollTime(self.clock.clockSpeed)

    def fastButton(self):                      #Changes the clock speed to fast
        self.changeActiveButton("Fast", GuiFormatter.speedGroup)
        self.clock.speedF()
        self.app.setPollTime(self.clock.clockSpeed)

    def gradesButton(self):                    #Open "carmen" subwindow
        self.app.showSubWindow("Carmen", hide = True)

    def reportCardButton(self):                #Open "Report Card" subwindow
        self.app.showSubWindow("ReportCard", hide = True)

    #General functions

    def changeActiveButton(self, activeBtn, group):  #Turns the active button green, changes all others in group to black
        for btn in group:
            self.app.setButtonFg(btn, "Black")
        self.app.setButtonFg(activeBtn, "Green")

    def changeActiveAction(self, activeAction):      #Turns the active action to True, others to False
        for act in self.student.studentState:
            self.student.studentState[act] = False
        self.student.studentState[activeAction] = True

    def updateHUD(self, day, hour, student):         #Funtions sent to processTick, runs everytime the clock ticks
        self.app.setLabel("lb1", "Day: " + str(day) + "\tHour: " + str(hour))
        self.app.setMeter("Experience", student.exp)
        self.app.setMeter("Stress", student.stress)
        if student.exp == 0:
            self.app.setLabel("expLabel", "Experience (Level " + str(student.expLevel) + ")")
        self.app.setLabel("DayOfWeek", str(Clock.WEEK_DAYS[day % 7]))

    def getStudentName(self):                        #Prompts player to enter their name, passes it to student
        name = self.app.stringBox("Welcome To OSU!", "Please Type Name Below")
        if name == None or name.isspace() or len(name) == 0:
            self.app.warningBox("Invalid Entry", "Please Enter Name")
            name = self.getStudentName()
        return name

    def saveGame(self):                              #TODO: Exports a file that saves gamestate to be opened later
        print(self.student.name)

    def ready(self):                                 #Launch the GUI window
        self.app.go()


class SaveState:
    def __init__(self):
        self.save = False

    @staticmethod
    def saveGame(gameState):
        pass

    @staticmethod
    def loadGame(gameState):
        pass


class Student:

    def __init__(self):

        self.studentState = {'studying': False, 'sleeping': True, 'relaxing': False}
        self.name = 'John Doe'
        self.expLevel = 1
        self.exp = 0
        self.stress = 0
        self.energy = 100
        self.stressRate = 1.5    #per hour
        self.expRate = 1.5       #per hour
        self.friend = False

    def getExpRate(self):
        if self.friend:
            return self.expRate * (1/self.expLevel) * 1.25
        else:
            return self.expRate * (1/self.expLevel)

    def getStressRate(self):
        if self.friend and self.studentState['studying']:
            return self.stressRate * 0.75
        else:
            return self.stressRate

    def stressTick(self):
        if self.studentState['studying']:
            self.stress += self.stressRate
        if self.studentState['relaxing']:
            self.stress -= self.stressRate
        if self.studentState['sleeping']:
            self.stress -= 0.5*self.stressRate
        if self.stress < 0:
            self.stress = 0

    def expTick(self):
        if self.studentState['studying']:
            self.exp += self.getExpRate()
        if self.exp >= 100:
            self.exp = 0
            self.expLevel += 1


#Start the game
x = Game()

#TODO:
#Add functionality to energy level (in student)
#   Go from 100 to 75 over course of normal day (16 hours)
#   Include popup warning when you haven't sleept in a long time (at 50?)
#   below 50 increases stress, decreases exp gain
#   below 25, increases stress, decreases exp gain further

#Start on script
#   Create Script file that can be called by GuiFormatter

#If stress reaches 100, game is over

#Overall improvement to layout
#   Figure out the best layout for buttons
#   Where will text be displayed?
#   Seperators between button groups
#   Name entry box needs script and should be loaded on center of screen

#Determine how to save and load the game
#   need gameState dict which contains all important info (day, hour, exp, report card....)

#Stretch goal: Include functionality to allow player to create a weekly schedule
#   pre-set actions for certain times and then let the program autorun their schedule

#Create Math class which will handle all requests for probablilities and other advanced calculations
#   consider moving getExpRate and getStressRate to Math class

#Create Course class
