##############################################################################
# Created by: Sabrina Poulsen                                                #
#                                                                            #
# See https://github.com/SRPoulsen/Physics-6810-Project for revision history #
#                                                                            #
# This file contains all the information for the unique courses the player   #
# takes over the 4 years at OSU. imported into main.py and used by Course    #
# class to fill the information out when creating an instance of course.     #
#                                                                            #
##############################################################################

import calculations as calc

def mechOne():
    courseName = 'Mechanics One'
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClassTime()
    endTime = startTime + 1
    difficulty = 1.0
    importantDates = [30, 60]
    hwDueDate = calc.scheduleHwDate(meetingDays)
    return [courseName, meetingDays, startTime, endTime, difficulty, importantDates, hwDueDate]

def emOne():
    courseName = 'E&M One'
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClassTime()
    endTime = startTime + 1
    difficulty = 1.0
    importantDates = [30, 60]
    hwDueDate = calc.scheduleHwDate(meetingDays)
    return [courseName, meetingDays, startTime, endTime, difficulty, importantDates, hwDueDate]

def labOne():
    courseName = 'Intro Lab'
    meetingDays = ['Monday', 'Wednesday', 'Friday']
    startTime = calc.scheduleClassTime()
    endTime = startTime + 3
    difficulty = 2.0
    importantDates = [20, 40, 60]
    hwDueDate = calc.scheduleHwDate(meetingDays)

    return [courseName, meetingDays, startTime, endTime, difficulty, importantDates, hwDueDate]

def quantum():
    courseName = 'Quantum Mechanics'
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClassTime()
    endTime = startTime + 1
    difficulty = 2.0
    importantDates = [30, 60]
    hwDueDate = calc.scheduleHwDate(meetingDays)
    return [courseName, meetingDays, startTime, endTime, difficulty, importantDates, hwDueDate]

def mechTwo():
    courseName = 'Mechanics Two'
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClassTime()
    endTime = startTime + 1
    difficulty = 3.0
    importantDates = [30, 60]
    hwDueDate = calc.scheduleHwDate(meetingDays)
    return [courseName, meetingDays, startTime, endTime, difficulty, importantDates, hwDueDate]

def emTwo():
    courseName = 'E&M Two'
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClassTime()
    endTime = startTime + 1
    difficulty = 3.0
    importantDates = [30, 60]
    hwDueDate = calc.scheduleHwDate(meetingDays)
    return [courseName, meetingDays, startTime, endTime, difficulty, importantDates, hwDueDate]

def seniorLab():
    courseName = 'Senior Lab'
    meetingDays = ['Monday', 'Wednesday', 'Friday']
    startTime = calc.scheduleClassTime()
    endTime = startTime + 3
    difficulty = 4.0
    importantDates = [20, 40, 60]
    hwDueDate = calc.scheduleHwDate(meetingDays)
    return [courseName, meetingDays, startTime, endTime, difficulty, importantDates, hwDueDate]

def statMech():
    courseName = 'Statistical Mechanics'
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClassTime()
    endTime = startTime + 1
    difficulty = 4.0
    importantDates = [30, 60]
    hwDueDate = calc.scheduleHwDate(meetingDays)
    return [courseName, meetingDays, startTime, endTime, difficulty, importantDates, hwDueDate]
