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

def scheduleClass():
    randNum = random.random()
    if randNum < 0.25:
        return 8
    if randNum >= 0.25 and randNum < 0.75:
        return 9
    if randNum >= 0.75:
        return 10
