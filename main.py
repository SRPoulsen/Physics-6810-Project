##############################################################################
# Created by: Sabrina Poulsen                                                #
#                                                                            #
# See https://github.com/SRPoulsen/Physics-6810-Project for revision history #
#                                                                            #
# This file contains the main framework of the game, as well as the command  #
# to actually intialize and run the game. This file is the one that should   #
# be run in terminal to play the game.                                       #
#                                                                            #
##############################################################################

from appJar import gui
import script
import courseInfo
import calculations as calc

class Game:
    started = False
    COURSE_LIST = [courseInfo.mechOne(), courseInfo.emOne(), courseInfo.labOne(), courseInfo.quantum(), \
                  courseInfo.mechTwo(), courseInfo.emTwo(), courseInfo.seniorLab(), courseInfo.statMech()]
    FINAL_GRADES = []

    def __init__(self):

        self.student = Student()
        self.clock = Clock(self.processTick)
        self.gui = GuiFormatter(self.clock, self.student, self.gatherGameState, self.gatherGrades)

        self.gameState = []            #Will store all important info about the game (date, name, grade, stress, exp...)
        self.turnedInHw = False        #Prevents processTick from turning in too much homework

        self.gui.ready()               #Launches gui after everything else has been processed

    def processTick(self, day, hour):  #Main method: Processes all functions that need to update every hour/tick

        # Recalculate every hour and update the HUD #
        self.student.expTick()
        self.student.stressTick()
        self.student.energyTick()
        self.gui.updateHUD(day, hour, self.student)

        # If it's the beginning of a new semester, change the course you're in #
        if Clock.newSemester and self.clock.semester <= 8:
            self.startNewSemester()

        # Confirms that the game has started and a course has been created #
        Game.started = True

        # Turn in homework every week #
        self.turnInHomework()

        # If the student is too stressed, end the game #
        if self.student.isTooStressed:
            self.gui.gameOver()

        # If the student makes it to the last semester, end the game #
        if self.clock.semester > 8 and Clock.newSemester:
            self.gui.gameWin()

    def startNewSemester(self):
        if Game.started:
            Game.FINAL_GRADES.append(self.course.getGrade())
            print('\nFinal Grades:' + str(Game.FINAL_GRADES))
        self.course = Course(Game.COURSE_LIST[self.clock.semester - 1], self.clock, self.student)
        print(script.newCourseIntro(self.course))
        Clock.newSemester = False

    def turnInHomework(self):
        if str(Clock.WEEK_DAYS[self.clock.clockDay % 7]) == self.course.hwDueDate and not self.turnedInHw:
            self.course.addHomeworkGrade()
            self.turnedInHw = True
        if str(Clock.WEEK_DAYS[self.clock.clockDay % 7]) != self.course.hwDueDate:
            self.turnedInHw = False

    def gatherGrades(self):
        grade = self.course.getGrade()
        print(grade)

    def gatherGameState(self):
        studentInfo = self.student.gatherStudentInfo()
        clockInfo = self.clock.gatherClockInfo()
        self.gameState = [studentInfo, clockInfo]
        print("Information Gathered")
        print(self.gameState)


class GuiFormatter:
    created = False                             #There has never been a created GUI before

    #Groups of buttons where only one button from each group is allowed to be active
    speedGroup = ['Slow', 'Medium', 'Fast']
    timeGroup = ['Play', 'Pause']
    actionGroup = ['Study', 'Relax', 'Sleep']

    def __init__(self, clk, ss, gi, gg):
        if GuiFormatter.created:            #Only allows one GUI to be created
            raise Exception('Instance already exists')

        GuiFormatter.created = True          #There has now been a created GUI
        self.clock = clk                     #Save the instance of the clock
        self.student = ss                    #Save the instance of the student
        self.gatherInfo = gi                 #Trigger "gatherGameState" in Game
        self.getGrades = gg                  #Trigger "gatherGrades" in Game

        #Calls on functions (below) to create and format the gui, as well as subWindows
        self.createAndFormatGui()
        self.createDateTimeDisplay()
        self.createStatusIndicators()
        self.createGuiButtons()
        self.addSeperators()
        self.initializeSubWindow("Carmen", script.carmen(self.student.expLevel))
        self.initializeSubWindow("Report Card", "This is a test of the report card")
        self.initializeSubWindow("Help", script.helpWindow())

        #Initialize the clock to run at "slow" speed, then begin looping through runClock
        self.app.setPollTime(self.clock.clockSpeed)
        self.app.registerEvent(self.clock.runClock)

        #Prompt user for their name, passes name to student
        #self.student.name = self.getStudentName()

    # GUI formatting and initialization functions #

    def createAndFormatGui(self):              #Creates and formats the main gui
        self.app = gui("Control Window")
        self.app.setSize(700,600)
        self.app.setLocation(650, 100)
        self.app.setFont(20)
        self.app.setStretch("both")
        self.app.setSticky("news")
        self.app.setGuiPadding(50, 5)
        self.app.setBg("WhiteSmoke")

    def createDateTimeDisplay(self):           #Creates the Date and Time display on gui
        self.app.setSticky("")
        self.app.addLabel("PauseLabel", "Paused", 1, 2)
        self.app.setLabelFg("PauseLabel", "red")
        self.app.addLabel("dateLabel", "Day: 0\tTime: 12 AM", 1, 1)
        self.app.addLabel("DayOfWeek", "Sunday", 1, 0)
        self.app.setLabelWidth("PauseLabel", 50)
        self.app.setLabelWidth("dateLabel", 50)
        self.app.setLabelWidth("DayOfWeek", 50)

    def createGuiButtons(self):                #Creates all the buttons for gui
        self.app.setSticky("nsew")
        self.app.addButton("Study", self.studyButton, 6, 0)
        self.app.addButton("Relax", self.relaxButton, 6, 1)
        self.app.addButton("Sleep", self.sleepButton, 6, 2)
        self.app.setButtonFg("Sleep", "Green")
        self.app.addButton("Play", self.playButton, 7, 0)
        self.app.addButton("Pause", self.pauseButton, 7, 1)
        self.app.addButton("Save", self.saveButton, 7, 2)
        self.app.addButton("Slow", self.slowButton, 8, 0)
        self.app.addButton("Medium", self.medButton, 8, 1)
        self.app.addButton("Fast", self.fastButton, 8, 2)
        self.app.setButtonFg("Slow", "Green")
        self.app.addButton("Grades", self.gradesButton, 9, 0)
        self.app.addButton("Report Card", self.reportCardButton, 9, 1)
        self.app.addButton("Help", self.helpButton, 9, 2)

    def addSeperators(self):
        self.app.addHorizontalSeparator(0,0,3, colour="Black")
        self.app.addHorizontalSeparator(5,0,3, colour="Black")

    def createStatusIndicators(self):          #Creates the meters and labels that tell the players their stats on gui
        self.app.setSticky("ew")
        self.app.addLabel("expLabel", "Experience (Level 1)", 2, 0, 1)
        self.app.addLabel("engLabel", "Energy", 3, 0, 1)
        self.app.addLabel("strLabel", "Stress", 4, 0, 1)
        self.app.addMeter("Experience", 2, 1, 2)
        self.app.setMeterFill("Experience", "Green")
        self.app.addMeter("Energy", 3, 1, 2)
        self.app.setMeterFill("Energy", "MediumBlue")
        self.app.setMeter("Energy", 100)
        self.app.addMeter("Stress", 4, 1, 2)
        self.app.setMeterFill("Stress", "Red")

    def initializeSubWindow(self, label, text):    #Creates a subWindow then immediatly hides it
        self.app.startSubWindow(label, modal = False)
        self.app.setFont(15)
        self.app.addMessage(label + "Label", text)
        #self.app.setSize(400,600)
        self.app.setLocation(100, 100)
        self.app.stopSubWindow()

    # Button functions #

    def playButton(self):                      #When the "Play" button is pressed, start the clock
        self.app.setLabel("PauseLabel", " ")
        self.changeActiveButton("Play", GuiFormatter.timeGroup)
        self.clock.startClock()

    def pauseButton(self):                     #When the "Pause" button is pressed, stop the clock
        self.app.setLabel("PauseLabel", "Paused")
        self.changeActiveButton("Pause", GuiFormatter.timeGroup)
        self.clock.stopClock()

    def saveButton(self):
        self.gatherInfo()

    def studyButton(self):                     #Changes studying to true, changes relax/sleep to false
        self.changeActiveAction('studying')
        self.changeActiveButton("Study", GuiFormatter.actionGroup)

    def relaxButton(self):                     #Changes relaxing to true, changes study/sleep to false
        self.changeActiveAction('relaxing')
        self.changeActiveButton("Relax", GuiFormatter.actionGroup)

    def sleepButton(self):                     #Changes sleeping to true, changes study/relax to false
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
        '''self.app.destroySubWindow("Carmen")
        self.initializeSubWindow("Carmen", script.carmen(self.student.expLevel))
        self.app.showSubWindow("Carmen", hide = True)'''
        if Game.started:
            self.getGrades()
        else:
            pass

    def reportCardButton(self):                #Open "Report Card" subwindow
        self.app.destroySubWindow("Report Card")
        self.initializeSubWindow("Report Card", "This is a test of the report card")
        self.app.showSubWindow("Report Card", hide = True)

    def helpButton(self):                      #Open "Help" subwindow
        self.app.showSubWindow("Help", hide = True)

    # General functions #

    def changeActiveButton(self, activeBtn, group):  #Turns the active button green, changes all others in group to black
        for btn in group:
            self.app.setButtonFg(btn, "Black")
        self.app.setButtonFg(activeBtn, "Green")

    def changeActiveAction(self, activeAction):      #Turns the active action to True, others to False
        for act in self.student.studentState:
            self.student.studentState[act] = False
        self.student.studentState[activeAction] = True

    def updateHUD(self, day, hour, student):         #Funtions sent to processTick, runs everytime the clock ticks
        self.app.setLabel("dateLabel", "Day: " + str(day) + str(self.clock.militaryToAmPm(hour)))
        self.app.setMeter("Experience", student.exp)
        self.app.setMeter("Stress", student.stress)
        self.app.setMeter("Energy", student.energy)
        if student.exp == 0:
            self.app.setLabel("expLabel", "Experience (Level " + str(student.expLevel) + ")")
        self.app.setLabel("DayOfWeek", str(Clock.WEEK_DAYS[day % 7]))

    def getStudentName(self):                        #Prompts player to enter their name, passes it to student
        self.app.setLocation(650, 100)
        name = self.app.stringBox("Welcome To OSU!", "Please Type Name Below")
        if name == None or name.isspace() or len(name) == 0:
            self.app.warningBox("Invalid Entry", "Please Enter Name")
            name = self.getStudentName()
        return name

    def saveGame(self):                              #TODO: Exports a file that saves gamestate to be opened later
        print(self.student.name)

    def ready(self):                                 #Launch the gui window
        self.app.go()

    def gameOver(self):                              #Alerts player that they've lost, destroys gui
        self.app.warningBox("Game Over", "Sorry! You Lost.")
        self.app.stop()

    def gameWin(self):
        self.app.warningBox("You Win", "Congratulations! You've won the game!")
        self.app.stop()


class Clock:
    WEEK_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    newSemester = True

    def __init__(self, act):
        self.clockDay = 0
        self.clockHour = 0             #Start at hour = 0
        self.semester = 1              #8 total semesters (4 years)
        self.clockIsRunning = False    #Start with the clock paused
        self.clockSpeed = 1000         #1000 ms delay on clock (1 s)
        self.action = act              #Passes in the action that should be performed every loop of runClock

    def startClock(self):          #Changes the status to "clock is running"
        if not self.clockIsRunning:             #Makes sure the clock wasn't already running
            self.clockIsRunning = True

    def stopClock(self):           #Changes the status to "clock isn't running"
        self.clockIsRunning = False

    def runClock(self):
        if self.clockIsRunning:                    #Makes sure the clock is running and the date is unlocked
            self.clockHour += 1                    #Adds one hour to the clock
            if self.clockHour >= 24:
                self.clockHour -= 24
                self.clockDay += 1
            if self.clockDay >= Course.semesterLength + 1:
                self.clockDay = 0
                self.semester += 1
                Clock.newSemester = True
            self.action(self.clockDay, self.clockHour)   #action = processTick in Game class

    def speedS(self):              #Slowest speed (1 hour per second)
        self.clockSpeed = 1000

    def speedM(self):              #Middle speed
        self.clockSpeed = 500

    def speedF(self):              #Fasted speed
        self.clockSpeed = 50

    def militaryToAmPm(self, hour): #Takes in miltiary time, returns time in AM or PM as string
        if hour < 12 and hour != 0:
            return "\tTime: " + str(hour) + " AM"
        if hour == 12:
            return "\tTime: 12 PM"
        if hour == 0:
            return "\tTime: 12 AM"
        else:
            return "\tTime: " + str(hour - 12) + " PM"

    def gatherClockInfo(self):
        day = self.clockDay
        hr = self.clockHour
        sem = self.semester
        return [day, hr, sem]


class Student:
    stressBaseRate = 1.5    #per hour
    expBaseRate = 5         #per hour
    energyBaseRate = 1.5    #per hour

    def __init__(self):

        self.studentState = {'studying': False, 'sleeping': True, 'relaxing': False}
        self.name = 'John Doe'
        self.expLevel = 1
        self.exp = 0
        self.stress = 0
        self.energy = 100
        self.isTooStressed = False
        self.friend = False

    def getExpRate(self):
        if self.friend:
            return Student.expBaseRate * (1/self.expLevel) * 1.25
        else:
            return Student.expBaseRate * (1/self.expLevel)

    def getStressRate(self):
        if self.friend and self.studentState['studying']:
            return Student.stressBaseRate * 0.75
        else:
            return Student.stressBaseRate

    def getEnergyRate(self):
        if self.studentState['studying']:
            return -Student.energyBaseRate
        if self.studentState['relaxing']:
            return Student.energyBaseRate
        if self.studentState['sleeping']:
            return Student.energyBaseRate * 5

    def stressTick(self):
        if self.studentState['studying']:
            self.stress += self.getStressRate()
        if self.studentState['relaxing']:
            self.stress -= self.getStressRate()
        if self.studentState['sleeping']:
            self.stress -= 0.25*self.getStressRate()
        if self.stress < 0:
            self.stress = 0
        if self.stress >= 100:
            #self.isTooStressed = True
            self.stress = 100

    def expTick(self):
        if self.studentState['studying']:
            self.exp += self.getExpRate()
        if self.exp > 100:
            self.exp = 0
            self.expLevel += 1

    def energyTick(self):
        self.energy += self.getEnergyRate()
        if self.energy > 100:
            self.energy = 100
        if self.energy < 0:
            self.energy = 0

    def gatherStudentInfo(self):
        nm = self.name
        ss = self.studentState
        lvl = self.expLevel
        exp = self.exp
        sts = self.stress
        eng = self.energy
        frd = self.friend
        return [nm, ss, lvl, exp, sts, eng, frd]


class Course:
    semesterLength = 20

    def __init__(self, cls, clk, stu):

        self.clock = clk
        self.student = stu
        self.courseName = cls[0]
        self.meetingDays = cls[1]
        self.startTime = cls[2]
        self.endTime = cls[3]
        self.difficulty = cls[4]
        self.importantDates = cls[5]
        self.hwDueDate = cls[6]
        self.grades = []

    def addHomeworkGrade(self):
        self.grades.append(calc.homeworkGrade(self.student))

    def getGrade(self):
        if len(self.grades) == 0:
            return "No Grades Yet"
        else:
            print(self.grades)
            return calc.calculateGrade(self.grades)


class SaveState:          #TODO: Nothing in this class works yet, do not call or interact with
    def __init__(self):
        self.save = False

    @staticmethod
    def saveGame(gameState):
        pass

    @staticmethod
    def loadGame(gameState):
        pass


#Start the game
x = Game()

#Testing Notes:
#   Fast speed set to 50 instead of 250 (Clock speedF function)
#   Tick rate for exp and stress is too fast (Student __init__ function)
#   Name Entry Disabled (GuiFormatter __init__ function)
#   Game over is disabled, instead caps stress at 100 (Student stressTick function)
#   energy alerts disabled (GuiFormatter updateHUD function)
#   Grades button functionality changed (GuiFormatter gradesButton function)
#   Return all the currect grades, not the total grade (Course getGrade function)
#   Semester length is shorter (Course variable)


#TODO:
##Add functionality to energy level (in student)
#   Go from 100 to 75 over course of normal day (16 hours)
#   Include popup warning when you haven't sleept in a long time (at 50?)
#   below 50 increases stress, decreases exp gain
#   below 25, increases stress, decreases exp gain further
##Start on script
#   Create Script file that can be called by GuiFormatter
##Overall improvement to layout
#   Figure out the best layout for buttons
#   Where will text be displayed?
#   Name entry box needs script and should be loaded on center of screen
##Determine how to save and load the game
#   need gameState dict which contains all important info (day, hour, exp, report card....)
##Stretch goal: Include functionality to allow player to create a weekly schedule
#   pre-set actions for certain times and then let the program autorun their schedule
##Create Calculations library which will handle all requests for probablilities and other advanced calculations
#   consider moving getExpRate and getStressRate to math library
##Create Course class
##When Game is over, instead of closing the Gui right away, tell the player their stats
##Going to need a "pack up" function which returns a list of strings
#   These lists will get passed to functions in script.py in order to fill out things like the report card
##Eventually, the subwindows might need their own initialization functions since they might be different sizes and stuff
##Make hwDueDate in courseInfo.py random
