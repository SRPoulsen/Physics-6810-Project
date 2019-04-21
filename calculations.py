##############################################################################
# Created by: Sabrina Poulsen                                                #
#                                                                            #
# See https://github.com/SRPoulsen/Physics-6810-Project for revision history #
#                                                                            #
# This file contains all the function which define major calculations. This  #
# file is imported into main.py.                                             #
#                                                                            #
##############################################################################

import numpy as np
import random
import math

def scheduleClassTime():           #Randomly assigns your class to be at 8 am (25%), 9 am (50%), or 10 am (25%)
    randNum = random.random()
    if randNum < 0.25:
        return 8
    if randNum >= 0.25 and randNum < 0.75:
        return 9
    if randNum >= 0.75:
        return 10

def scheduleHwDate(meetingDays):
    return random.choice(meetingDays)

def homeworkGrade(student, difficulty):
    center = 9 + student.expLevel + (student.exp / 100) - difficulty
    std = student.stress / 50
    grade = round(np.random.normal(center, std), 2)
    if grade > 10:
        grade = 10

    return [grade, 10]

def testGrade(student, difficulty):
    center = 40 + (((1.5 * student.expLevel + (student.exp / 100)) - difficulty) * 4)
    std = student.stress / 8
    grade = round(np.random.normal(center, std), 2)
    if grade > 50:
        grade = 50

    return [grade, 50]

def calculateGrade(gradesList):    #Takes in a list of lists, calculates the grade the student currently has
    studentPoints = 0
    totalPoints = 0
    for _, value in gradesList.items():
        studentPoints += value[0]
        totalPoints += value[1]

    return round((float(studentPoints) / float(totalPoints)) * 100, 2)
