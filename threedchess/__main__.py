#!/bin/python3

from direct.stdpy import threading
import os
import sys
import traceback
import time
from math import *

from .lib import game
from .lib import rendering_task
from .lib import print_controls

##

def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    print('Press any key to exit.')
    input()
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

##

#game = game(0,1,(8,))
game = game(1,1,(8,8))
#game = game(2,0,(8,8))
#game = game(2,1,(8,8,8))

# Move to command line task
while True:
    print('Load from a saved file? (y/n)')
    savefile = input()
    print('')
    if savefile == 'y':
        game.open()
        break
    elif savefile == 'n':
        print_controls()
        game.restart()
        break
    else:
        print('This is not a valid selection\n')

from .lib import main_menu
main_menu.game = game

## Main task
thread = threading.Thread(target = main_menu.open, args = ())
thread.start()


## Panda3d task
#Fix input
game.renders[0].run()
