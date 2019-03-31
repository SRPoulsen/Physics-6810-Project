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
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClass()
    endTime = startTime + 1
    difficulty = 1
    importantDates = [30, 60]
    return [meetingDays, startTime, endTime, difficulty, importantDates]

def emOne():
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClass()
    endTime = startTime + 1
    difficulty = 1
    importantDates = [30, 60]
    return [meetingDays, startTime, endTime, difficulty, importantDates]

def labOne():
    meetingDays = ['Monday', 'Wednesday', 'Friday']
    startTime = calc.scheduleClass()
    endTime = startTime + 3
    difficulty = 2
    importantDates = [20, 40, 60]

    return [meetingDays, startTime, endTime, difficulty, importantDates]

def quantum():
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClass()
    endTime = startTime + 1
    difficulty = 2
    importantDates = [30, 60]
    return [meetingDays, startTime, endTime, difficulty, importantDates]

def mechTwo():
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClass()
    endTime = startTime + 1
    difficulty = 3
    importantDates = [30, 60]
    return [meetingDays, startTime, endTime, difficulty, importantDates]

def emTwo():
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClass()
    endTime = startTime + 1
    difficulty = 3
    importantDates = [30, 60]
    return [meetingDays, startTime, endTime, difficulty, importantDates]

def seniorLab():
    meetingDays = ['Monday', 'Wednesday', 'Friday']
    startTime = calc.scheduleClass()
    endTime = startTime + 3
    difficulty = 4
    importantDates = [20, 40, 60]
    return [meetingDays, startTime, endTime, difficulty, importantDates]

def statMech():
    meetingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    startTime = calc.scheduleClass()
    endTime = startTime + 1
    difficulty = 4
    importantDates = [30, 60]
    return [meetingDays, startTime, endTime, difficulty, importantDates]