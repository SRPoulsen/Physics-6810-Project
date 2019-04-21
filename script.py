##############################################################################
# Created by: Sabrina Poulsen                                                #
#                                                                            #
# See https://github.com/SRPoulsen/Physics-6810-Project for revision history #
#                                                                            #
# This file contains all the text used in the game. Each word block is       #
# a callable function which returns the text in one long string.             #
#                                                                            #
##############################################################################

def helpWindow():
    message = "-- Buttons -- \
            \nStudy: Student will study, causing experience and stress to increase and energy to decrease \
            \nRelax: Student will relax, causing stess to decrease (rapidly) and energy to increase (slowly) \
            \nSleep: Student will sleep, causing energy to increase (rapidly) and stress to decrease (slowly) \
            \nPlay: Causes time to move forward \
            \nPause: Stops time from moving \
            \nGrades: Displays grades from your current class, as well as final grades in previous classes \
            \nSlow: Causes time to move slowly \
            \nMedium: Cause time to move moderatly fast \
            \nFast: Causes time to move very fast \
            \nSave: Saves your game so you can load it later \
            \nLoad: Load a previous save file"
    return message

def gradesWindow(grades):
    #message = "The students experience level is " + str(expLvl)
    #return message
    pass

def newCourseIntro(course):
    message = "\nWelcome to " + str(course.courseName) + "!"
    message += "\nYour class will be held at " + str(course.startTime) + " AM on " + str(course.meetingDays)
    message += "\nHomework is due every " + str(course.hwDueDate)
    message += "\nYou have tests on day " + str(course.importantDates)

    return message
