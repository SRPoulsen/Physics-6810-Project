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
import courseInfo as cInfo
import calculations as calc
import os
import json

class Game:
    started = False       #The game is not started yet (turns true when clock starts ticking)
    COURSE_LIST = [cInfo.mechOne(), cInfo.emOne(), cInfo.labOne(), cInfo.quantum(), \
                   cInfo.mechTwo(), cInfo.emTwo(), cInfo.seniorLab(), cInfo.statMech()]  #The courses you take in order
    FINAL_GRADES = {}     #Final grades from each class are stored here
    ALL_GRADES = {}       #Every homework and test grade will be saved here at the end of the semeseter

    def __init__(self):

        # Create all the instances (except courses, which is made in processTick) #
        self.student = Student()
        self.clock = Clock(self.processTick)
        self.gui = GuiFormatter(self.clock, self.student, self.gatherGameState, self.loadGameState, self.gatherGrades, self.returnCourseInfo)
        self.saveState = SaveState()

        self.gameState = []            #Will store all important info about the game (date, name, grade, stress, exp...)
        self.turnedInHw = False        #Prevents processTick from turning in too much homework
        self.tookTest = False          #Prevents processTick from taking too many tests
        self.inClass = False           #Flag to keep track of if you're in class or not

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

        # See if current day of the week and time is during class #
        self.checkIfInClass()

        # Everytime class is held the difficulty increases #
        if self.inClass:
            self.course.increaseDifficulty()
            print(self.course.difficulty)

        # Turn in homework every week and take tests on important days #
        self.turnInHomework()
        self.takeTest()

        # If the student is too tired, they have to sleep #
        if self.student.isTooTired and not GuiFormatter.energyAlertGiven:
            self.gui.tiredPlayerAlert()
            self.gui.sleepButton()

        # If the student is too stressed, end the game #
        if self.student.isTooStressed:
            self.gui.gameOverStress()

        # If the student makes it to the last semester, end the game #
        if self.clock.semester > 8 and Clock.newSemester:
            self.gui.gameWin()

    def checkIfInClass(self):
        if (str(Clock.WEEK_DAYS[self.clock.clockDay % 7]) in self.course.meetingDays) and (self.clock.clockHour == self.course.startTime):
            self.inClass = True
        if (str(Clock.WEEK_DAYS[self.clock.clockDay % 7]) not in self.course.meetingDays) or (self.clock.clockHour != self.course.startTime):
            self.inClass = False

    def startNewSemester(self):
        if Game.started:          #Doesn't try and save grades when starting the first semester
            Game.ALL_GRADES[self.course.courseName] = self.course.grades          #Save grades as hash {course : grade}
            finalGrade = self.course.getGrade()
            Game.FINAL_GRADES[self.course.courseName] = finalGrade                #Save grades as hash {course : grade}
            print('\nFinal Grades:' + str(Game.FINAL_GRADES))
            if finalGrade < 70.0:
                self.gui.gameOverFailed()

        self.course = Course(Game.COURSE_LIST[self.clock.semester - 1], self.clock, self.student)
        self.student.expLevel = 1
        self.student.exp = 0
        self.gui.updateHUD(self.clock.clockDay, self.clock.clockHour, self.student)
        self.returnCourseInfo()
        Clock.newSemester = False

    def returnCourseInfo(self):
        self.gui.newSemesterMessage(self.course)

    def turnInHomework(self):
        if self.inClass and str(Clock.WEEK_DAYS[self.clock.clockDay % 7]) == self.course.hwDueDate and not self.turnedInHw:
            self.course.addHomeworkGrade()
            self.turnedInHw = True
        if str(Clock.WEEK_DAYS[self.clock.clockDay % 7]) != self.course.hwDueDate:
            self.turnedInHw = False

    def takeTest(self):
        if self.clock.clockDay in self.course.importantDates and self.inClass and not self.tookTest:
            self.course.addTestGrade()
            self.tookTest = True
        if self.clock.clockDay not in self.course.importantDates:
            self.tookTest = False

    def gatherGrades(self):
        return [self.course.grades, self.course.getGrade(), Game.FINAL_GRADES]

    def gatherGameState(self, fileName):
        # Make sure the game has started before letting the player save the game #
        if Game.started:
            studentInfo = self.student.gatherStudentInfo()
            clockInfo = self.clock.gatherClockInfo()
            courseInfo = self.course.gatherCourseInfo()
            self.gameState = [studentInfo, clockInfo, courseInfo, Game.FINAL_GRADES, Game.ALL_GRADES]
            print("Information Gathered")
            self.saveState.save(self.gameState, fileName)
        else:
            print("Game has not been started. Press 'play' to start the game.")

    def loadGameState(self, fileName):
        # Have saveState.load retrieve data from json file #
        loadedData = self.saveState.load(fileName)

        # Override current data with the newly loaded data #
        self.loadStudentInfo(loadedData['student'])
        self.loadClockInfo(loadedData['clock'])
        self.loadCourseInfo(loadedData['course'])
        Game.FINAL_GRADES = loadedData['FINAL_GRADES']
        Game.ALL_GRADES = loadedData['ALL_GRADES']
        Game.started = True

        # Update the gui with the newly loaded data #
        self.gui.updateHUDafterLoad(self.clock, self.student)

    def loadStudentInfo(self, info):
        self.student.name = info[0]
        self.student.studentState = info[1]
        self.student.expLevel = info[2]
        self.student.exp = info[3]
        self.student.stress = info[4]
        self.student.energy = info[5]
        self.student.isTooTired = info[6]

    def loadClockInfo(self, info):
        self.clock.clockDay = info[0]
        self.clock.clockHour = info[1]
        self.clock.semester = info[2]
        Clock.newSemester = info[3]

    def loadCourseInfo(self, info):
        if not Game.started:
            self.course = Course(Game.COURSE_LIST[self.clock.semester - 1], self.clock, self.student)

        self.course.courseName = info[0]
        self.course.meetingDays = info[1]
        self.course.startTime = info[2]
        self.course.endTime = info[3]
        self.course.difficulty = info[4]
        self.course.importantDates = info[5]
        self.course.hwDueDate = info[6]
        self.course.grades = info[7]
        self.course.hwNumber = info[8]
        self.course.testNumber = info[9]

class GuiFormatter:
    created = False                             #There has never been a created GUI before

    #Groups of buttons where only one button from each group is allowed to be active
    speedGroup = ['Slow', 'Medium', 'Fast']
    timeGroup = ['Play', 'Pause']
    actionGroup = ['Study', 'Relax', 'Sleep']

    energyAlertGiven = False

    def __init__(self, clk, ss, gi, lg, gg, sci):
        if GuiFormatter.created:            #Only allows one GUI to be created
            raise Exception('Instance already exists')

        GuiFormatter.created = True          #There has now been a created GUI
        self.clock = clk                     #Save the instance of the clock
        self.student = ss                    #Save the instance of the student
        self.gatherInfo = gi                 #Trigger "gatherGameState" in Game
        self.loadInfo = lg                   #Trigger "loadGameState" in Game
        self.getGrades = gg                  #Trigger "gatherGrades" in Game
        self.showCourseInfo = sci            #Trigger "returnCourseInfo" in Game

        #Calls on functions (below) to create and format the gui, as well as subWindows
        self.createAndFormatGui()
        self.createDateTimeDisplay()
        self.createStatusIndicators()
        self.createGuiButtons()
        self.addSeperators()
        self.initializeSubWindow("UnusedWindow", "")

        #Initialize the clock to run at "slow" speed, then begin looping through runClock
        self.app.setPollTime(self.clock.clockSpeed)
        self.app.registerEvent(self.clock.runClock)

        #Prompt user for their name, passes name to student
        self.student.name = self.getStudentName()
        self.app.infoBox('Welcome to OSU!', script.welcomeWindow(self.student.name))

    # GUI formatting and initialization functions #

    def createAndFormatGui(self):                  #Creates and formats the main gui
        self.app = gui("Control Window")
        self.app.setSize(700,600)
        self.app.setLocation(650, 100)
        self.app.setFont(20)
        self.app.setStretch("both")
        self.app.setSticky("news")
        self.app.setGuiPadding(50, 5)
        self.app.setBg("WhiteSmoke")

    def createDateTimeDisplay(self):               #Creates the Date and Time display on gui
        self.app.setSticky("")
        self.app.addLabel("PauseLabel", "Paused", 1, 2)
        self.app.setLabelFg("PauseLabel", "red")
        self.app.addLabel("dateLabel", "Day: 0\tTime: 12 AM", 1, 1)
        self.app.addLabel("DayOfWeek", "Sunday", 1, 0)
        self.app.setLabelWidth("PauseLabel", 50)
        self.app.setLabelWidth("dateLabel", 50)
        self.app.setLabelWidth("DayOfWeek", 50)

    def createGuiButtons(self):                    #Creates all the buttons for gui
        self.app.setSticky("nsew")
        self.app.addButton("Study", self.studyButton, 6, 0)
        self.app.addButton("Relax", self.relaxButton, 6, 1)
        self.app.addButton("Sleep", self.sleepButton, 6, 2)
        self.app.setButtonFg("Sleep", "Green")
        self.app.addButton("Play", self.playButton, 7, 0)
        self.app.addButton("Pause", self.pauseButton, 7, 1)
        self.app.addButton("Grades", self.gradesButton, 7, 2)
        self.app.addButton("Slow", self.slowButton, 8, 0)
        self.app.addButton("Medium", self.medButton, 8, 1)
        self.app.addButton("Fast", self.fastButton, 8, 2)
        self.app.setButtonFg("Slow", "Green")
        self.app.addButton("Save", self.saveButton, 9, 0)
        self.app.addButton("Load", self.loadButton, 9, 1)
        self.app.addButton("Current Course Info", self.ccButton, 9, 2)

    def addSeperators(self):                       #Creates the lines which sepreate the buttons from the HUD
        self.app.addHorizontalSeparator(0,0,3, colour="Black")
        self.app.addHorizontalSeparator(5,0,3, colour="Black")

    def createStatusIndicators(self):              #Creates the meters and labels that tell the players their stats on gui
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


    def studyButton(self):                     #Changes studying to true, changes relax/sleep to false
        if not self.student.isTooTired:
            self.changeActiveAction('studying')
            self.changeActiveButton("Study", GuiFormatter.actionGroup)
        else:
            pass

    def relaxButton(self):                     #Changes relaxing to true, changes study/sleep to false
        if not self.student.isTooTired:
            self.changeActiveAction('relaxing')
            self.changeActiveButton("Relax", GuiFormatter.actionGroup)
        else:
            pass

    def sleepButton(self):                     #Changes sleeping to true, changes study/relax to false
        self.changeActiveAction('sleeping')
        self.changeActiveButton("Sleep", GuiFormatter.actionGroup)

    def playButton(self):                      #When the "Play" button is pressed, start the clock
        self.app.setLabel("PauseLabel", " ")
        self.changeActiveButton("Play", GuiFormatter.timeGroup)
        self.clock.startClock()

    def pauseButton(self):                     #When the "Pause" button is pressed, stop the clock
        self.app.setLabel("PauseLabel", "Paused")
        self.changeActiveButton("Pause", GuiFormatter.timeGroup)
        self.clock.stopClock()

    def gradesButton(self):                    #Open grades subwindow
        if Game.started:
            self.app.infoBox("Grades", script.gradesWindow(self.getGrades()))
        else:
            pass

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

    def saveButton(self):                      #Calls getSaveFileName() then passes that file name to Game
        fileName = self.getSaveFileName()
        self.gatherInfo(fileName)

    def loadButton(self):                      #Trigger loading the game
        nameAndPath = self.getLoadFileName()
        if nameAndPath == 'DoNotLoadGame':
            pass
        else:
            self.loadInfo(nameAndPath)

    def ccButton(self):                      #Open "Current Course Info" alert
        if Game.started:
            self.showCourseInfo()
        else:
            pass

    # General functions #

    def changeActiveButton(self, activeBtn, group):  #Turns the active button green, changes all others in group to black
        for btn in group:
            self.app.setButtonFg(btn, "Black")
        self.app.setButtonFg(activeBtn, "Green")

    def changeActiveAction(self, activeAction):      #Turns the active action to True, others to False
        for act in self.student.studentState:
            self.student.studentState[act] = False
        self.student.studentState[activeAction] = True

    def updateHUD(self, day, hour, student):         #Function sent to processTick, runs everytime the clock ticks
        self.app.setLabel("dateLabel", "Day: " + str(day) + str(self.clock.militaryToAmPm(hour)))
        self.app.setMeter("Experience", student.exp)
        self.app.setMeter("Stress", student.stress)
        self.app.setMeter("Energy", student.energy)
        if student.exp == 0:
            self.app.setLabel("expLabel", "Experience (Level " + str(student.expLevel) + ")")
        self.app.setLabel("DayOfWeek", str(Clock.WEEK_DAYS[day % 7]))

    def updateHUDafterLoad(self, clock, student):    #After loading a game, update the HUD before the clock starts
        self.app.warningBox("Game Loaded", "The game has been successfully loaded.")
        self.app.setLabel("dateLabel", "Day: " + str(clock.clockDay) + str(self.clock.militaryToAmPm(clock.clockHour)))
        self.app.setLabel("DayOfWeek", str(Clock.WEEK_DAYS[clock.clockDay % 7]))
        self.app.setLabel("expLabel", "Experience (Level " + str(student.expLevel) + ")")
        self.app.setMeter("Experience", student.exp)
        self.app.setMeter("Stress", student.stress)
        self.app.setMeter("Energy", student.energy)

    def getStudentName(self):                        #Prompts player to enter their name, passes it to student
        self.app.setLocation(650, 100)
        name = self.app.stringBox("Welcome To OSU!", "Please Type Name Below")
        if name == None or name.isspace() or len(name) == 0:
            self.app.warningBox("Invalid Entry", "Please Enter Name")
            name = self.getStudentName()
        return name

    def getSaveFileName(self):                       #Prompts player to enter a name for their save file
        self.app.setLocation(650, 100)
        fileName = self.app.stringBox("Preparing To Save Game", "Please type the name of your save file.")
        if fileName == None or fileName.isspace() or len(fileName) == 0:
            self.app.warningBox("Invalid Entry", "File was not saved.")
            pass
        return fileName

    def getLoadFileName(self):                       #Prompts player to choose a save file to load
        dir = str(os.path.dirname(os.path.abspath(__file__))) + "/save_files/"
        nameAndPath = self.app.openBox(title= 'Choose File to Load', dirName = dir, fileTypes = [('text', '*.txt')])
        if not (dir in nameAndPath) and len(nameAndPath) != 0:
             self.app.warningBox("Invalid Entry", "Only files from saved_files may be loaded. Please choose from starting directory.")
             nameAndPath = self.getLoadFileName()
        if len(nameAndPath) == 0:
            return 'DoNotLoadGame'
        return nameAndPath

    def tiredPlayerAlert(self):
        self.app.warningBox("You Fell Asleep!", script.tiredPlayer())
        GuiFormatter.energyAlertGiven = True

    def newSemesterMessage(self, course):
        self.app.infoBox("Welcome to your new class!", script.newCourseIntro(course))

    def ready(self):                                 #Launch the gui window
        self.app.go()

    def gameOverStress(self):                        #Alerts player that they've lost because they are too stressed, destroys gui
        self.app.warningBox("Game Over", "Sorry! You Lost.")
        self.app.stop()

    def gameOverFailed(self):                        #Alerts the player that they've lost because they fail their class, destroys gui
        self.app.warningBox("Game Over", "Sorry! You Lost.")
        self.app.stop()

    def gameWin(self):                               #Alerts player that they've won the game, destroys gui
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
        self.clockSpeed = 700          #750 ms delay on clock
        self.action = act       #Passes in the action that should be performed every loop of runClock

    def startClock(self):           #Changes the status to "clock is running"
        if not self.clockIsRunning:             #Makes sure the clock wasn't already running
            self.clockIsRunning = True

    def stopClock(self):            #Changes the status to "clock isn't running"
        self.clockIsRunning = False

    def runClock(self):             #Repeatidly calls process tick at the end of the loop (self.action)
        if self.clockIsRunning:                    #Makes sure the clock is running and the date is unlocked
            self.clockHour += 1                    #Adds one hour to the clock
            if self.clockHour >= 24:               #Flips to next day after 24 hours
                self.clockHour -= 24
                self.clockDay += 1
            if self.clockDay >= Course.semesterLength + 1:   #Flips to next semester after it's over
                self.clockDay = 0
                self.semester += 1
                Clock.newSemester = True                     #Tells processTick to create the next course instance
            self.action(self.clockDay, self.clockHour)

    def speedS(self):               #Slowest speed (1 hour per second)
        self.clockSpeed = 700

    def speedM(self):               #Middle speed
        self.clockSpeed = 300

    def speedF(self):               #Fasted speed
        self.clockSpeed = 75

    def militaryToAmPm(self, hour): #Takes in miltiary time, returns time in AM or PM as string
        if hour < 12 and hour != 0:
            return "\tTime: " + str(hour) + " AM"
        if hour == 12:
            return "\tTime: 12 PM"
        if hour == 0:
            return "\tTime: 12 AM"
        else:
            return "\tTime: " + str(hour - 12) + " PM"

    def gatherClockInfo(self):      #Collects all information that needs to be saved, gives it to Game as a list
        day = self.clockDay
        hr = self.clockHour
        sem = self.semester
        ns = Clock.newSemester
        return [day, hr, sem, ns]


class Student:
    stressBaseRate = 0.5    #per hour
    expBaseRate = 2.0       #per hour
    energyBaseRate = 1.0    #per hour

    def __init__(self):

        self.studentState = {'studying': False, 'sleeping': True, 'relaxing': False}
        self.name = 'John Doe'
        self.expLevel = 1
        self.exp = 0
        self.stress = 0
        self.energy = 100
        self.isTooStressed = False
        self.isTooTired = False

    def getExpRate(self):
        return Student.expBaseRate * (1/self.expLevel)

    def getStressRate(self):
        return Student.stressBaseRate

    def getEnergyRate(self):
        if self.studentState['studying']:
            return -Student.energyBaseRate * 1.5
        if self.studentState['relaxing']:
            return Student.energyBaseRate
        if self.studentState['sleeping']:
            if self.isTooTired:
                return Student.energyBaseRate * 2.5
            else:
                return Student.energyBaseRate * 5

    def stressTick(self):
        if self.studentState['studying']:
            self.stress += self.getStressRate()
        if self.studentState['relaxing']:
            self.stress -= self.getStressRate() * 2
        if self.studentState['sleeping']:
            self.stress -= 0.25*self.getStressRate()
        if self.stress < 0:
            self.stress = 0
        if self.stress >= 100:
            self.isTooStressed = True
            self.stress = 100

    def expTick(self):
        if self.studentState['studying']:
            self.exp += self.getExpRate()
        if self.exp > 100:
            self.exp = 0
            self.expLevel += 1

    def energyTick(self):
        self.energy += self.getEnergyRate()
        if self.energy > 100:              #Upper limit for energy is 100
            self.energy = 100
        if self.energy < 0:                #Lower limit for energy is 0
            self.energy = 0
            self.isTooTired = True                    #If energy = 0, you are too tired to do anything except sleep
        if self.isTooTired and self.energy == 100:    #Once you've refilled your energy, you are not too tired anymore
            self.isTooTired = False
            GuiFormatter.energyAlertGiven = False

    def gatherStudentInfo(self):
        nm = self.name
        ss = self.studentState
        lvl = self.expLevel
        exp = self.exp
        sts = self.stress
        eng = self.energy
        itt = self.isTooTired
        return [nm, ss, lvl, exp, sts, eng, itt]


class Course:
    semesterLength = 62

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
        self.hwNumber = 1
        self.testNumber = 1
        self.grades = {}

    def addHomeworkGrade(self):
        key = 'Homework #' + str(self.hwNumber)
        self.grades[key] = (calc.homeworkGrade(self.student, self.difficulty))
        self.hwNumber += 1

    def addTestGrade(self):
        key = 'Test #' + str(self.testNumber)
        self.grades[key] = (calc.testGrade(self.student, self.difficulty))
        self.testNumber += 1

    def getGrade(self):
        if len(self.grades) == 0:
            return "No Grades Yet"
        else:
            return calc.calculateGrade(self.grades)

    def increaseDifficulty(self):
        self.difficulty += 0.15

    def gatherCourseInfo(self):
        cn = self.courseName
        md = self.meetingDays
        st = self.startTime
        et = self.endTime
        df = self.difficulty
        id = self.importantDates
        hw = self.hwDueDate
        gr = self.grades
        hn = self.hwNumber
        tn = self.testNumber


        return [cn, md, st, et, df, id, hw, gr, hn, tn]


class SaveState:

    def __init__(self):
        self.path = str(os.path.dirname(os.path.abspath(__file__))) + "/save_files/"

    def save(self, gameState, fileName):
        # Create the full path to the save_files folder #
        fileNameAndPath = self.path + str(fileName) + '.txt'

        # Save the gamestate as a dict, easier for json to read and dump #
        saveinfo = {}
        saveinfo['student'] = gameState[0]
        saveinfo['clock'] = gameState[1]
        saveinfo['course'] = gameState[2]
        saveinfo['FINAL_GRADES'] = gameState[3]
        saveinfo['ALL_GRADES'] = gameState[4]

        # Create the json file and fill it #
        with open(fileNameAndPath, 'w') as savefile:
            json.dump(saveinfo, savefile)

        savefile.close()

    def load(self, fileName):

        # Open the file and save it as 'loadedData' #
        with open(fileName) as json_file:
            loadedData = json.load(json_file)

        return loadedData

#Start the game
x = Game()

#Testing Notes:
#   slow speed set to 10 instead of 750 (Clock speedS function)
#   Tick rate for exp and stress is too fast (Student __init__ function)
#   Grades button functionality changed (GuiFormatter gradesButton function)


#TODO:
##Add functionality to energy level (in student)
#   Go from 100 to 75 over course of normal day (16 hours)
#   below 50 increases stress, decreases exp gain
#   below 25, increases stress, decreases exp gain further
##Continue on script
##Overall improvement to layout
#   Figure out the best layout for buttons
#   Where will text be displayed?
##Stretch goal: Include functionality to allow player to create a weekly schedule
#   pre-set actions for certain times and then let the program autorun their schedule
##When Game is over, instead of closing the Gui right away, tell the player their stats
##Going to need a "pack up" function which returns a list of strings
#   These lists will get passed to functions in script.py in order to fill out things like the report card
##Eventually, the subwindows might need their own initialization functions since they might be different sizes and stuff

##Important info that needs to be saved/loaded
#   student
#       Name
#       studentState
#       expLevel
#       exp
#       stress
#       energy
#       isTooTired
#   clock
#       clockDay
#       clockHour
#       semester
#       Clock.newSemester
#   course
#       courseName
#       meetingDays
#       startTime
#       endTime
#       difficulty
#       importantDates
#       hwDueDate
#       grades
#   game
#       FINAL_GRADES
