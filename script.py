##############################################################################
# Created by: Sabrina Poulsen                                                #
#                                                                            #
# See https://github.com/SRPoulsen/Physics-6810-Project for revision history #
#                                                                            #
# This file contains all the text used in the game. Each word block is       #
# a callable function which returns the text in one long string.             #
#                                                                            #
##############################################################################

def welcomeWindow(studentName):
    message = "Hello, " + str(studentName) + ", and welcome to your first semester as a physics major at OSU!\n\n"
    message += "You'll be starting your first class tomorrow, and if you want to succeed you'll need to study hard. Be careful, though! "
    message += "If you stress yourself out too much, it's game over!\n\n"
    message += "For help on how to play the game (including current course information), click the 'Help' button"

    return message

def newCourseIntro(course):
    stringWeekDays = ''
    for day in course.meetingDays:
        stringWeekDays += '\n' + str(day)

    stringTestDays = ''
    for day in course.importantDates:
        stringTestDays += '\n' + str(day)

    message = "\nWelcome to " + str(course.courseName) + "!"
    message += "\n\nYour class will be held at " + str(course.startTime) + " AM on" + stringWeekDays
    message += "\n\nHomework is due every " + str(course.hwDueDate)
    message += "\n\nYou have tests on days " + stringTestDays

    return message

def helpWindow(course):
    message = ""
    return message

def gradesWindow(grades):
    message = "-- Assigment Grades --\n\n"
    for key in grades[0]:
        if "Test" in str(key):
            message += str(key) + "\t\t\t" + str(grades[0][key][0]) + "/" + str(grades[0][key][1]) + "\n"
        else:
            message += str(key) + "\t" + str(grades[0][key][0]) + "/" + str(grades[0][key][1]) + "\n"
    message += "\nCurrent Grade = " + str(grades[1])

    message += "\n\n-- Final Grades --\n\n"
    for key in grades[2]:
        message += str(key) + ":\t" + str(grades[2][key])

    return message

def tiredPlayer():
    message = "Oh no! Looks like you stayed up too long. You were so tired that you fell asleep, \
               and you won't be able to study again until you've gotten a good nights rest!"

    return message
