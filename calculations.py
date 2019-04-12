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

def scheduleClass():           #Randomly assigns your class te be at 8 am (25%), 9 am (50%), or 10 am (25%)
    randNum = random.random()
    if randNum < 0.25:
        return 8
    if randNum >= 0.25 and randNum < 0.75:
        return 9
    if randNum >= 0.75:
        return 10

def homeworkGrade():
    return [10,10]

def testGrade():
    pass

def calculateGrade(gradesList):    #Takes in a list of lists, calculates the grade the student currently has
    studentPoints = 0
    totalPoints = 0

    for i in range(len(gradesList)):
        studentPoints += gradesList[i][0]
        totalPoints += gradesList[i][1]

    return float(studentPoints) / float(totalPoints)
