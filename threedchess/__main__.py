#!/bin/python3

import threading
import os
import sys
import traceback
import time
from math import *

from .lib import rendering_task

##

def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    print('Press any key to exit.')
    input()
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

##

class piecec:
    def __init__(self,typ,pos,col):
        self.atr = {'typ':typ,'pos':pos,'col':col,'first':0,'moved_last_turn':False,'ispicked1':False,'ispicked2':False}

##

class game():
    def restart(self):
        print('Controls:')
        print('Space to go up')
        print('"z" to go down')
        print('"w" to go foward')
        print('"s" to go back')
        print('"a" to go left')
        print('"d" to go right')
        print('"c" to teleport to white\'s start')
        print('"v" to teleport to black\'s start')
        print('"i" to tilt camera up')
        print('"k" to tilt camera down')
        print('"j" to tilt camera left')
        print('"l" to tilt camera right')
        print('Left click to select the piece you want to move')
        print('Right click to select the square/piece you want to move to')
        print('Enter to move the selected piece to the selected square')
        print('')
        print('Input:')
        print('Input should be the coordinates of the thing you want to move,')
        print('a space,')
        print('then the coordinates of where you want to move it to.')
        print('Coordinates are written as a letter from a-g specifying column from left to right')
        print('followed by a number form 1-8 specifying row from front to back')
        print('and finally a letter form s-z specifying plane from bottom to top')
        print('ex:a7u c5u\n')

        self.turn = 1
        self.capturedposw = 0
        self.capturedposb = 0
        self.moved_from_last_turn = [None,None,None]
        self.enpass = [None,None,None]
        self.gameover = 0

        self.king1 = piecec('king',[5, 1, 1],1)
        self.pawn1 = piecec('pawn',[1, 3, 2],1)
        self.pawn2 = piecec('pawn',[2, 3, 2],1)
        self.pawn3 = piecec('pawn',[3, 3, 2],1)
        self.pawn4 = piecec('pawn',[4, 3, 2],1)
        self.pawn5 = piecec('pawn',[5, 3, 2],1)
        self.pawn6 = piecec('pawn',[6, 3, 2],1)
        self.pawn7 = piecec('pawn',[7, 3, 2],1)
        self.pawn8 = piecec('pawn',[8, 3, 2],1)
        self.pawn9 = piecec('pawn',[1, 2, 3],1)
        self.pawn10 = piecec('pawn',[2, 2, 3],1)
        self.pawn11 = piecec('pawn',[3, 2, 3],1)
        self.pawn12 = piecec('pawn',[4, 2, 3],1)
        self.pawn13 = piecec('pawn',[5, 2, 3],1)
        self.pawn14 = piecec('pawn',[6, 2, 3],1)
        self.pawn15 = piecec('pawn',[7, 2, 3],1)
        self.pawn16 = piecec('pawn',[8, 2, 3],1)
        self.peasant1 = piecec('peasant',[1, 3, 1],1)
        self.peasant2 = piecec('peasant',[2, 3, 1],1)
        self.peasant3 = piecec('peasant',[3, 3, 1],1)
        self.peasant4 = piecec('peasant',[4, 3, 1],1)
        self.peasant5 = piecec('peasant',[5, 3, 1],1)
        self.peasant6 = piecec('peasant',[6, 3, 1],1)
        self.peasant7 = piecec('peasant',[7, 3, 1],1)
        self.peasant8 = piecec('peasant',[8, 3, 1],1)
        self.peasant9 = piecec('peasant',[1, 1, 3],1)
        self.peasant10 = piecec('peasant',[2, 1, 3],1)
        self.peasant11 = piecec('peasant',[3, 1, 3],1)
        self.peasant12 = piecec('peasant',[4, 1, 3],1)
        self.peasant13 = piecec('peasant',[5, 1, 3],1)
        self.peasant14 = piecec('peasant',[6, 1, 3],1)
        self.peasant15 = piecec('peasant',[7, 1, 3],1)
        self.peasant16 = piecec('peasant',[8, 1, 3],1)
        self.soldier1 = piecec('soldier',[1, 3, 3],1)
        self.soldier2 = piecec('soldier',[2, 3, 3],1)
        self.soldier3 = piecec('soldier',[3, 3, 3],1)
        self.soldier4 = piecec('soldier',[4, 3, 3],1)
        self.soldier5 = piecec('soldier',[5, 3, 3],1)
        self.soldier6 = piecec('soldier',[6, 3, 3],1)
        self.soldier7 = piecec('soldier',[7, 3, 3],1)
        self.soldier8 = piecec('soldier',[8, 3, 3],1)
        self.knight1 = piecec('knight',[1, 2, 1],1)
        self.knight2 = piecec('knight',[4, 2, 2],1)
        self.knight3 = piecec('knight',[5, 2, 2],1)
        self.knight4 = piecec('knight',[8, 2, 1],1)
        self.horse1 = piecec('horse',[1, 2, 2],1)
        self.horse2 = piecec('horse',[2, 2, 1],1)
        self.horse3 = piecec('horse',[7, 2, 1],1)
        self.horse4 = piecec('horse',[8, 2, 2],1)
        self.elephant1 = piecec('elephant',[1, 1, 2],1)
        self.elephant2 = piecec('elephant',[2, 2, 2],1)
        self.elephant3 = piecec('elephant',[7, 2, 2],1)
        self.elephant4 = piecec('elephant',[8, 1, 2],1)
        self.rook1 = piecec('rook',[1, 1, 1],1)
        self.rook2 = piecec('rook',[3, 2, 2],1)
        self.rook3 = piecec('rook',[6, 2, 2],1)
        self.rook4 = piecec('rook',[8, 1, 1],1)
        self.bishop1 = piecec('bishop',[2, 1, 2],1)
        self.bishop2 = piecec('bishop',[3, 2, 1],1)
        self.bishop3 = piecec('bishop',[6, 2, 1],1)
        self.bishop4 = piecec('bishop',[7, 1, 2],1)
        self.cardinal1 = piecec('cardinal',[2, 1, 1],1)
        self.cardinal2 = piecec('cardinal',[3, 1, 2],1)
        self.cardinal3 = piecec('cardinal',[6, 1, 2],1)
        self.cardinal4 = piecec('cardinal',[7, 1, 1],1)
        self.queen1 = piecec('queen',[3, 1, 1],1)
        self.queen2 = piecec('queen',[6, 1, 1],1)
        self.duchess1 = piecec('duchess',[4, 1, 2],1)
        self.duchess2 = piecec('duchess',[5, 1, 2],1)
        self.princess1 = piecec('princess',[4, 2, 1],1)
        self.princess2 = piecec('princess',[5, 2, 1],1)
        self.pope1 = piecec('pope',[4, 1, 1],1)
        self.king2 = piecec('king',[5, 8, 8],-1)
        self.pawn17 = piecec('pawn',[1, 6, 7],-1)
        self.pawn18 = piecec('pawn',[2, 6, 7],-1)
        self.pawn19 = piecec('pawn',[3, 6, 7],-1)
        self.pawn20 = piecec('pawn',[4, 6, 7],-1)
        self.pawn21 = piecec('pawn',[5, 6, 7],-1)
        self.pawn22 = piecec('pawn',[6, 6, 7],-1)
        self.pawn23 = piecec('pawn',[7, 6, 7],-1)
        self.pawn24 = piecec('pawn',[8, 6, 7],-1)
        self.pawn25 = piecec('pawn',[1, 7, 6],-1)
        self.pawn26 = piecec('pawn',[2, 7, 6],-1)
        self.pawn27 = piecec('pawn',[3, 7, 6],-1)
        self.pawn28 = piecec('pawn',[4, 7, 6],-1)
        self.pawn29 = piecec('pawn',[5, 7, 6],-1)
        self.pawn30 = piecec('pawn',[6, 7, 6],-1)
        self.pawn31 = piecec('pawn',[7, 7, 6],-1)
        self.pawn32 = piecec('pawn',[8, 7, 6],-1)
        self.peasant17 = piecec('peasant',[1, 6, 8],-1)
        self.peasant18 = piecec('peasant',[2, 6, 8],-1)
        self.peasant19 = piecec('peasant',[3, 6, 8],-1)
        self.peasant20 = piecec('peasant',[4, 6, 8],-1)
        self.peasant21 = piecec('peasant',[5, 6, 8],-1)
        self.peasant22 = piecec('peasant',[6, 6, 8],-1)
        self.peasant23 = piecec('peasant',[7, 6, 8],-1)
        self.peasant24 = piecec('peasant',[8, 6, 8],-1)
        self.peasant25 = piecec('peasant',[1, 8, 6],-1)
        self.peasant26 = piecec('peasant',[2, 8, 6],-1)
        self.peasant27 = piecec('peasant',[3, 8, 6],-1)
        self.peasant28 = piecec('peasant',[4, 8, 6],-1)
        self.peasant29 = piecec('peasant',[5, 8, 6],-1)
        self.peasant30 = piecec('peasant',[6, 8, 6],-1)
        self.peasant31 = piecec('peasant',[7, 8, 6],-1)
        self.peasant32 = piecec('peasant',[8, 8, 6],-1)
        self.soldier9 = piecec('soldier',[1, 6, 6],-1)
        self.soldier10 = piecec('soldier',[2, 6, 6],-1)
        self.soldier11 = piecec('soldier',[3, 6, 6],-1)
        self.soldier12 = piecec('soldier',[4, 6, 6],-1)
        self.soldier13 = piecec('soldier',[5, 6, 6],-1)
        self.soldier14 = piecec('soldier',[6, 6, 6],-1)
        self.soldier15 = piecec('soldier',[7, 6, 6],-1)
        self.soldier16 = piecec('soldier',[8, 6, 6],-1)
        self.knight5 = piecec('knight',[1, 7, 8],-1)
        self.knight6 = piecec('knight',[4, 7, 7],-1)
        self.knight7 = piecec('knight',[5, 7, 7],-1)
        self.knight8 = piecec('knight',[8, 7, 8],-1)
        self.horse5 = piecec('horse',[1, 7, 7],-1)
        self.horse6 = piecec('horse',[2, 7, 8],-1)
        self.horse7 = piecec('horse',[7, 7, 8],-1)
        self.horse8 = piecec('horse',[8, 7, 7],-1)
        self.elephant5 = piecec('elephant',[1, 8, 7],-1)
        self.elephant6 = piecec('elephant',[2, 7, 7],-1)
        self.elephant7 = piecec('elephant',[7, 7, 7],-1)
        self.elephant8 = piecec('elephant',[8, 8, 7],-1)
        self.rook5 = piecec('rook',[1, 8, 8],-1)
        self.rook6 = piecec('rook',[3, 7, 7],-1)
        self.rook7 = piecec('rook',[6, 7, 7],-1)
        self.rook8 = piecec('rook',[8, 8, 8],-1)
        self.bishop5 = piecec('bishop',[2, 8, 7],-1)
        self.bishop6 = piecec('bishop',[3, 7, 8],-1)
        self.bishop7 = piecec('bishop',[6, 7, 8],-1)
        self.bishop8 = piecec('bishop',[7, 8, 7],-1)
        self.cardinal5 = piecec('cardinal',[2, 8, 8],-1)
        self.cardinal6 = piecec('cardinal',[3, 8, 7],-1)
        self.cardinal7 = piecec('cardinal',[6, 8, 7],-1)
        self.cardinal8 = piecec('cardinal',[7, 8, 8],-1)
        self.queen3 = piecec('queen',[3, 8, 8],-1)
        self.queen4 = piecec('queen',[6, 8, 8],-1)
        self.duchess3 = piecec('duchess',[4, 8, 7],-1)
        self.duchess4 = piecec('duchess',[5, 8, 7],-1)
        self.princess3 = piecec('princess',[4, 7, 8],-1)
        self.princess4 = piecec('princess',[5, 7, 8],-1)
        self.pope2 = piecec('pope',[4, 8, 8],-1)
        self.pieces = [self.king1,self.pawn1,self.pawn2,self.pawn3,self.pawn4,self.pawn5,self.pawn6,self.pawn7,self.pawn8,self.pawn9,self.pawn10,self.pawn11,self.pawn12,self.pawn13,self.pawn14,self.pawn15,self.pawn16,self.peasant1,self.peasant2,self.peasant3,self.peasant4,self.peasant5,self.peasant6,self.peasant7,self.peasant8,self.peasant9,self.peasant10,self.peasant11,self.peasant12,self.peasant13,self.peasant14,self.peasant15,self.peasant16,self.soldier1,self.soldier2,self.soldier3,self.soldier4,self.soldier5,self.soldier6,self.soldier7,self.soldier8,self.knight1,self.knight2,self.knight3,self.knight4,self.horse1,self.horse2,self.horse3,self.horse4,self.elephant1,self.elephant2,self.elephant3,self.elephant4,self.rook1,self.rook2,self.rook3,self.rook4,self.bishop1,self.bishop2,self.bishop3,self.bishop4,self.cardinal1,self.cardinal2,self.cardinal3,self.cardinal4,self.queen1,self.queen2,self.duchess1,self.duchess2,self.princess1,self.princess2,self.pope1,self.king2,self.pawn17,self.pawn18,self.pawn19,self.pawn20,self.pawn21,self.pawn22,self.pawn23,self.pawn24,self.pawn25,self.pawn26,self.pawn27,self.pawn28,self.pawn29,self.pawn30,self.pawn31,self.pawn32,self.peasant17,self.peasant18,self.peasant19,self.peasant20,self.peasant21,self.peasant22,self.peasant23,self.peasant24,self.peasant25,self.peasant26,self.peasant27,self.peasant28,self.peasant29,self.peasant30,self.peasant31,self.peasant32,self.soldier9,self.soldier10,self.soldier11,self.soldier12,self.soldier13,self.soldier14,self.soldier15,self.soldier16,self.knight5,self.knight6,self.knight7,self.knight8,self.horse5,self.horse6,self.horse7,self.horse8,self.elephant5,self.elephant6,self.elephant7,self.elephant8,self.rook5,self.rook6,self.rook7,self.rook8,self.bishop5,self.bishop6,self.bishop7,self.bishop8,self.cardinal5,self.cardinal6,self.cardinal7,self.cardinal8,self.queen3,self.queen4,self.duchess3,self.duchess4,self.princess3,self.princess4,self.pope2]
        self.piecess = ['king1','pawn1','pawn2','pawn3','pawn4','pawn5','pawn6','pawn7','pawn8','pawn9','pawn10','pawn11','pawn12','pawn13','pawn14','pawn15','pawn16','peasant1','peasant2','peasant3','peasant4','peasant5','peasant6','peasant7','peasant8','peasant9','peasant10','peasant11','peasant12','peasant13','peasant14','peasant15','peasant16','soldier1','soldier2','soldier3','soldier4','soldier5','soldier6','soldier7','soldier8','knight1','knight2','knight3','knight4','horse1','horse2','horse3','horse4','elephant1','elephant2','elephant3','elephant4','rook1','rook2','rook3','rook4','bishop1','bishop2','bishop3','bishop4','cardinal1','cardinal2','cardinal3','cardinal4','queen1','queen2','duchess1','duchess2','princess1','princess2','pope1','king2','pawn17','pawn18','pawn19','pawn20','pawn21','pawn22','pawn23','pawn24','pawn25','pawn26','pawn27','pawn28','pawn29','pawn30','pawn31','pawn32','peasant17','peasant18','peasant19','peasant20','peasant21','peasant22','peasant23','peasant24','peasant25','peasant26','peasant27','peasant28','peasant29','peasant30','peasant31','peasant32','soldier9','soldier10','soldier11','soldier12','soldier13','soldier14','soldier15','soldier16','knight5','knight6','knight7','knight8','horse5','horse6','horse7','horse8','elephant5','elephant6','elephant7','elephant8','rook5','rook6','rook7','rook8','bishop5','bishop6','bishop7','bishop8','cardinal5','cardinal6','cardinal7','cardinal8','queen3','queen4','duchess3','duchess4','princess3','princess4','pope2']

        self.create(f'{home}/public/pieces.txt',len(self.pieces))
        self.create(f'{home}/public/misc.txt',6)

        self.save = []
        for u in range(0,len(self.pieces)):
            self.save.append(self.piecess[u]+': '+f'[{self.pieces[u].atr["typ"]},({self.pieces[u].atr["pos"][0]},{self.pieces[u].atr["pos"][1]},{self.pieces[u].atr["pos"][2]}),{self.pieces[u].atr["col"]},{self.pieces[u].atr["first"]},{self.pieces[u].atr["moved_last_turn"]}]'+'\n')
        self.writer = open(f'{home}/public/pieces.txt', 'w')
        self.writer.writelines(self.save)
        self.writer.close()
        self.write(f'{home}/public/misc.txt','turn: ',str(self.turn),0)
        self.write(f'{home}/public/misc.txt','capturedposw: ',str(self.capturedposw),1)
        self.write(f'{home}/public/misc.txt','capturedposb: ',str(self.capturedposb),2)
        self.write(f'{home}/public/misc.txt','moved_from_last_turn: ',f'({self.moved_from_last_turn[0]},{self.moved_from_last_turn[1]},{self.moved_from_last_turn[2]})',3)
        self.write(f'{home}/public/misc.txt','enpass: ',f'({self.enpass[0]},{self.enpass[1]},{self.enpass[2]})',4)
        self.write(f'{home}/public/misc.txt','gameover: ',str(self.gameover),5)

    def open(self):
        print('Controls:')
        print('Space to go up')
        print('"z" to go down')
        print('"w" to go foward')
        print('"s" to go back')
        print('"a" to go left')
        print('"d" to go right')
        print('"c" to teleport to white\'s start')
        print('"v" to teleport to black\'s start')
        print('"i" to tilt camera up')
        print('"k" to tilt camera down')
        print('"j" to tilt camera left')
        print('"l" to tilt camera right')
        print('Left click to select the piece you want to move')
        print('Right click to select the square/piece you want to move to')
        print('Enter to move the selected piece to the selected square')
        print('')
        print('Input:')
        print('Input should be the coordinates of the thing you want to move,')
        print('a space,')
        print('then the coordinates of where you want to move it to.')
        print('Coordinates are written as a letter from a-g specifying column from left to right')
        print('followed by a number form 1-8 specifying row from front to back')
        print('and finally a letter form s-z specifying plane from bottom to top')
        print('ex:a7u c5u\n')

        self.pieces = []
        self.reader = open(f'{home}/public/pieces.txt','r')
        self.save = self.reader.readlines()
        for u in range(0,len(self.save)-1):
            self.pieces.append('')
            self.sp = self.split(self.save[u])
            self.pieces[u] = piecec(self.sp[0],self.sp[1],self.sp[2])
            self.pieces[u].atr['first'] = self.sp[3]
            self.pieces[u].atr['moved_last_turn'] = self.sp[4]
        self.reader.close()

        self.reader = open(f'{home}/public/misc.txt','r')
        self.save = self.reader.readlines()
        self.space = self.save[0].find(' ')
        self.turn = int(self.save[0][self.space+1:])
        self.space = self.save[1].find(' ')
        self.capturedposw = int(self.save[1][self.space+1:])
        self.space = self.save[2].find(' ')
        self.capturedposb = int(self.save[2][self.space+1:])
        self.left = self.save[3].find('(')
        self.right = self.save[3].find(')')
        self.moved_from_last_turn = self.save[3][self.left+1:self.right].split(',')
        for u in range(0,3):
            if self.moved_from_last_turn[u] == 'None':
                self.moved_from_last_turn[u] = None
            else:
                self.moved_from_last_turn[u] = int(self.moved_from_last_turn[u])
        self.left = self.save[4].find('(')
        self.right = self.save[4].find(')')
        self.enpass = self.save[4][self.left+1:self.right].split(',')
        for u in range(0,3):
            if self.enpass[u] == 'None':
                self.enpass[u] = None
            else:
                self.enpass[u] = int(self.enpass[u])
        self.space = self.save[5].find(' ')
        self.gameover = int(self.save[5][self.space+1:])
        self.reader.close()

    def create(self,file,length):
        try:
            os.remove(file)
        except:
            pass
        self.creater = open(file,'x')
        self.creater.close()
        self.writer = open(file,'w')
        self.writer.writelines('\n'*length)
        self.writer.close()

    def split(self,x):
        z = [None] * 5
        left = x.find('[')
        right = x.find(']')
        sc = x[left+1:right]
        left = sc.find('(')
        right = sc.find(')')
        z[1] = sc[left+1:right].split(',')
        sc = sc[:left-1] + sc[right+1:]
        sc = sc.split(',')
        z[0] = sc[0]
        z[1] = [int(u) for u in z[1]]
        z[2] = int(sc[1])
        z[3] = int(sc[2])
        if sc[3] == 'True':
            z[4] = True
        if sc[3] == 'False':
            z[4] = False
        return(z)

    def write(self,file,prefix,content,x):
        self.reader = open(file,'r')
        self.save = self.reader.readlines()
        self.space = self.save[x].find(' ')
        if prefix == None:
            self.name = self.save[x][0:self.space+1]
        else:
            self.name = prefix
        self.save[x] = (self.name+content+'\n')
        self.reader.close()
        self.writer = open(file,'w')
        self.writer.writelines(self.save)
        self.writer.close()

game = game()

##

class read():
    def stuff(self):
        while True:
            print('Enter:')
            print('"h" for help')
            print('"r" to restart')
            print('Or enter your move')
            h = input()
            print('')
            if game.gameover == 2:
                while True:
                    if h == 'y':
                        app.reset()
                        app.reset2()
                        move.ox = 0
                        move.oy = 0
                        move.oz = 0
                        move.nx = 0
                        move.ny = 0
                        move.nz = 0
                        app.unrenders()
                        app.unrendersboard()
                        game.restart()
                        app.rendersboard()
                        app.renders()
                        break
                    if h == 'n':
                        print('Thank you for playing!\n')
                        game.gameover = 1
                        break
                    else:
                        print('This is not a valid selection\n')
                        h = input()
                        print('')
                continue
            if h == 'help' or h == 'help!':
                self.helpmenu()
                continue
            if h == 'h':
                self.hellpmenu()
                continue
            if h == 'r':
                app.reset()
                app.reset2()
                move.ox = 0
                move.oy = 0
                move.oz = 0
                move.nx = 0
                move.ny = 0
                move.nz = 0
                app.unrenders()
                app.unrendersboard()
                game.restart()
                app.rendersboard()
                app.renders()
                continue
            if not len(h) == 7:
                print('Wrong number of characters\n')
                continue
            if not (h[0] == 'a' or h[0] == 'b' or h[0] == 'c' or h[0] == 'd' or h[0] == 'e' or h[0] == 'f' or h[0] == 'g' or h[0] == 'h'):
                print('The first character is incorrect\n')
                continue
            if not (h[1] == '1' or h[1] == '2' or h[1] == '3' or h[1] == '4' or h[1] == '5' or h[1] == '6' or h[1] == '7' or h[1] == '8'):
                print('The second character is incorrect\n')
                continue
            if not (h[2] == 's' or h[2] == 't' or h[2] == 'u' or h[2] == 'v' or h[2] == 'w' or h[2] == 'x' or h[2] == 'y' or h[2] == 'z'):
                print('The third character is incorrect\n')
                continue
            if not h[3] == ' ':
                print('The fourth character is incorrect\n')
                continue
            if not (h[4] == 'a' or h[4] == 'b' or h[4] == 'c' or h[4] == 'd' or h[4] == 'e' or h[4] == 'f' or h[4] == 'g' or h[4] == 'h'):
                print('The fifth character is incorrect\n')
                continue
            if not (h[5] == '1' or h[5] == '2' or h[5] == '3' or h[5] == '4' or h[5] == '5' or h[5] == '6' or h[5] == '7' or h[5] == '8'):
                print('The sixth character is incorrect\n')
                continue
            if not (h[6] == 's' or h[6] == 't' or h[6] == 'u' or h[6] == 'v' or h[6] == 'w' or h[6] == 'x' or h[6] == 'y' or h[6] == 'z'):
                print('The seventh character is incorrect\n')
                continue
            else:
                self.parse(h)
                move.findpiece()
                move.ox = 0
                move.oy = 0
                move.oz = 0
                move.nx = 0
                move.ny = 0
                move.nz = 0

    def helpmenu(self):
        print('''When I was younger so much younger than today\nI never needed anybody's help in any way\nBut now these days are gone, I'm not so self assured\nNow I find I've changed my mind and opened up the doors\nUh... You wanted a menu that helps gameplay? Nevermind this then. Press "h" to acess the other help menu\n''')

    def hellpmenu(self):
        while True:
            print('Welcome to the help menu')
            print('"w" to return to the previous menu')
            print('"c" to repeat basic controls')
            print('"b" to get basic chess rules')
            print('"d" to get a visual description to match each piece')
            print('"p" to get rules for the different pieces')
            print('"m" to see rules for special moves')
            h = input()
            print('')
            if h == 'w':
                return
            if h == 'c':
                print('Controls:')
                print('Space to go up')
                print('"z" to go down')
                print('"w" to go foward')
                print('"s" to go back')
                print('"a" to go left')
                print('"d" to go right')
                print('"c" to teleport to white\'s start')
                print('"v" to teleport to black\'s start')
                print('"i" to tilt camera up')
                print('"k" to tilt camera down')
                print('"j" to tilt camera left')
                print('"l" to tilt camera right')
                print('Left click to select the piece you want to move')
                print('Right click to select the square/piece you want to move to')
                print('Enter to move the selected piece to the selected square')
                print('')
                print('Input:')
                print('Input should be the coordinates of the thing you want to move,')
                print('a space,')
                print('then the coordinates of where you want to move it to.')
                print('Coordinates are written as a letter from a-g specifying column from left to right')
                print('followed by a number form 1-8 specifying row from front to back')
                print('and finally a letter form s-z specifying plane from bottom to top')
                print('ex:a7u c5u\n')
            if h == 'b':
                while True:
                    print('"w" to return to the previous menu')
                    print('"m" to see moving')
                    print('"c" to see capturing')
                    print('"v" to see winning the game')
                    h = input()
                    print('')
                    if h == 'm':
                        print('You must move one piece per turn. After you move it is your opponent\'s turn')
                        print('Pieces may move based on their move rules (see move rules)')
                        print('Most pieces, with a few notable exceptions, may not move through squares with pieces already in them')
                        print('You may not move pieces into squares you already have pieces in')
                        print('If you move into a square with one of your opponent\'s pieces that piece is captured (see capturing)\n')
                    if h == 'c':
                        print('If you move into a square with one of your opponent\'s piece that piece is taken off the board and can no longer be used or moved')
                        print('If you take the opponent\'s king the game is over and you have won (see winning the game)\n')
                    if h == 'v':
                        print('The goal of the game is to capture the opponent\'s king')
                        print('If the opponent\s king is captured you win')
                        print('If your king is captured your opponent wins')
                        print('Once a king has been captured the game is over')
                        print('Note that this 3d version does not have check, a rule used in traditional chess\n')
                    if h == 'w':
                        break
                continue
            if h == 'd':
                while True:
                    print('"w" to return to the previous menu')
                    print('Or enter the piece you want a visual description of')
                    print('Here is a list of pieces:')
                    print('king, pawn, peasant, soldier, knight, horse, elephant, rook, bishop, cardinal, queen, duchess, princess, pope')
                    h = input()
                    print('')
                    if h == 'king':
                        print('Two cones with a cross on top\n')
                    if h == 'pawn':
                        print('A cone with a sphere on top\n')
                    if h == 'peasant':
                        print('A cone with a sphere and hat on top holding a pitchfork\n')
                    if h == 'soldier':
                        print('A cone with a sphere and helmet on top holding a sword\n')
                    if h == 'knight':
                        print('A cone and cylinder with a cube and cylinder on top. Spheres for eyes. Looks like a horse\n')
                    if h == 'horse':
                        print('A cone with a helmet on top and conical pole. Looks like a knight\n')
                    if h == 'elephant':
                        print('A cone with a sphere on top. Spheres for eyes, cones for tusks, cylinder for trunk\n')
                    if h == 'rook':
                        print('A cylinder with a hollow cylinder on top. Looks like a castle\n')
                    if h == 'bishop':
                        print('A cone with a semi-sphere, cone and small sphere on top\n')
                    if h == 'cardinal':
                        print('A cone with a ring, semi-sphere and small sphere on top\n')
                    if h == 'queen':
                        print('A cone with a cylinder, cone and small sphere on top\n')
                    if h == 'duchess':
                        print('A cone with three cylinders on top\n')
                    if h == 'princess':
                        print('A cone with three cylinders, two semi-spheres and a small sphere on top\n')
                    if h == 'pope':
                        print('A cone with a semi-sphere and cross on top\n')
                    if h == 'w':
                        break
                continue
            if h == 'p':
                while True:
                    print('"w" to return to the previous menu')
                    print('Or enter the piece you want more information about')
                    print('Here is a list of pieces:')
                    print('king, pawn, peasant, soldier, knight, horse, elephant, rook, bishop, cardinal, queen, duchess, princess, pope')
                    h = input()
                    print('')
                    if h == 'king':
                        print('The king can move one square in any direction including all diagonals\n')
                        while True:
                            print('"w" to return to the previous menu')
                            print('"c" to see rules for castling')
                            print('Note that this 3d version does not have check, a rule used in traditional chess')
                            h = input()
                            print('')
                            if h == 'c':
                                print('To castle move your king two squares to the right or left and your rook will move to the square your king passed through')
                                print('Note that neither king nor rook can have moved yet during the game')
                                print('Also note that the rook jumping over the king is the only exception to the rule that the rook may not move through other pieces')
                                print('Another thing to consider is even though some other pieces move like rooks they can still not be used for castling\n')
                            if h == 'w':
                                break
                        continue
                    if h == 'pawn':
                        print('A pawn can move a square forward or up unless capturing where they must move sideway, and forward and/or up\n')
                        while True:
                            print('"w" to return to the previous menu')
                            print('"d" to see rules for the pawn double step')
                            print('"e" to see rules for en passant')
                            print('"p" to see rules for the pawn promotion')
                            h = input()
                            print('')
                            if h == 'd':
                                print('On a pawn\'s first move they may also move two squares forward or two squares up\n')
                            if h == 'e':
                                print('The turn directly after a pawn makes it\'s double step an opponent\'s pawn or peasant make capture the pawn not only in it\'s current location but also move into the square it passed through during it\'s double step to capture it\n')
                            if h == 'p':
                                print('When a pawn makes it to the other side of the board and the other side of the board vertically you must promote it to any piece except:')
                                print('king, pawn, peasant and soldier\n')
                            if h == 'w':
                                break
                        continue
                    if h == 'peasant':
                        print('A peasant can move a square forward and/or up unless capturing where they must move sideway, forward and up\n')
                        while True:
                            print('"w" to return to the previous menu')
                            print('"d" to see rules for the peasant double step')
                            print('"e" to see rules for en passant')
                            print('"p" to see rules for the peasant promotion')
                            h = input()
                            print('')
                            if h == 'd':
                                print('On a peasant\'s first move they may also move two squares forward, two squares up or two squares forward and two squares up\n')
                            if h == 'e':
                                print('The turn directly after a peasant makes it\'s double step an opponent\'s pawn or peasant make capture the peasant not only in it\'s current location but also move into the square it passed through during it\'s double step to capture it\n')
                            if h == 'p':
                                print('When a peasant makes it to the other side of the board and the other side of the board vertically you must promote it to any piece except:')
                                print('king, pawn, peasant, soldier\n')
                            if h == 'w':
                                break
                        continue
                    if h == 'soldier':
                        print('A soldier can move one square in any direction including all diagonals\n')
                    if h == 'knight':
                        print('A knight moves two squares in one direction and one square in a second direction')
                        print('Knights can also jump over (move through) pieces\n')
                    if h == 'horse':
                        print('A horse moves two squares in one direction and one square in a second and third direction')
                        print('Horses can also jump over (move through) pieces\n')
                    if h == 'elephant':
                        print('A elephant moves two squares in two directions and one square in a third direction')
                        print('Elephants can also jump over (move through) pieces\n')
                    if h == 'rook':
                        print('A rook can move any number of squares in one direction\n')
                    if h == 'bishop':
                        print('A bishop can move diagonally any number of squares in two directions and zero squares in a third direction')
                        print('Another way to think about is that the distance traveled in two directions must be the same and the distance traveled in the third direction must be zero')
                        print('Hint: Two of your bishops can only move along the darker squares and two of your bishops can only move along the lighter squares\n')
                    if h == 'cardinal':
                        print('A cardinal can move diagonally any number of squares in three directions')
                        print('Another way to think about is that the distance traveled in all three directions must be the same')
                        print('Hint: Each one of your cardinals can only move along one colour of square (Consider monochrome a colour for this process)\n')
                    if h == 'queen':
                        print('A queen may either move as a rook or a bishop')
                        print('See rules for those pieces for more details\n')
                    if h == 'duchess':
                        print('A duchess may either move as a rook or a cardinal')
                        print('See rules for those pieces for more details\n')
                    if h == 'princess':
                        print('A princess may either move as a bishop or a cardinal')
                        print('See rules for those pieces for more details\n')
                    if h == 'pope':
                        print('The pope may either move as a rook, a bishop or a cardinal')
                        print('See rules for those pieces for more details\n')
                    if h == 'w':
                        break
                continue
            if h == 'm':
                print('There are a few special moves to look out for')
                print('To see castling go to the king movement rules')
                print('Note that this 3d version does not have check, a rule used in traditional chess')
                print('To see pawn double step or pawn promotion go to the pawn movement rules')
                print('To see peasant double step or peasant promotion go to the peasant movement rules')
                print('To see en passant go to either the pawn or peasant movement rules\n')

    def parse(self,h):
        if h[0] == 'a':
            move.ox = 1
        if h[0] == 'b':
            move.ox = 2
        if h[0] == 'c':
            move.ox = 3
        if h[0] == 'd':
            move.ox = 4
        if h[0] == 'e':
            move.ox = 5
        if h[0] == 'f':
            move.ox = 6
        if h[0] == 'g':
            move.ox = 7
        if h[0] == 'h':
            move.ox = 8
        move.oy = int(h[1])
        if h[2] == 's':
            move.oz = 1
        if h[2] == 't':
            move.oz = 2
        if h[2] == 'u':
            move.oz = 3
        if h[2] == 'v':
            move.oz = 4
        if h[2] == 'w':
            move.oz = 5
        if h[2] == 'x':
            move.oz = 6
        if h[2] == 'y':
            move.oz = 7
        if h[2] == 'z':
            move.oz = 8
        if h[4] == 'a':
            move.nx = 1
        if h[4] == 'b':
            move.nx = 2
        if h[4] == 'c':
            move.nx = 3
        if h[4] == 'd':
            move.nx = 4
        if h[4] == 'e':
            move.nx = 5
        if h[4] == 'f':
            move.nx = 6
        if h[4] == 'g':
            move.nx = 7
        if h[4] == 'h':
            move.nx = 8
        move.ny = int(h[5])
        if h[6] == 's':
            move.nz = 1
        if h[6] == 't':
            move.nz = 2
        if h[6] == 'u':
            move.nz = 3
        if h[6] == 'v':
            move.nz = 4
        if h[6] == 'w':
            move.nz = 5
        if h[6] == 'x':
            move.nz = 6
        if h[6] == 'y':
            move.nz = 7
        if h[6] == 'z':
            move.nz = 8

class movement:
    def __init__(self):
        self.ox = 0
        self.oy = 0
        self.oz = 0
        self.nx = 0
        self.ny = 0
        self.nz = 0
        self.castlingvar = False

    def findpiece(self):
        self.enpass2 = [None,None,None]
        self.dx = abs(self.ox-self.nx)
        self.dy = abs(self.oy-self.ny)
        self.dz = abs(self.oz-self.nz)
        self.dl = sorted((self.dx,self.dy,self.dz))
        ip = 0
        for u in range(0,len(game.pieces)):
            if game.pieces[u].atr['pos'][0] == self.ox and game.pieces[u].atr['pos'][1] == self.oy and game.pieces[u].atr['pos'][2] == self.oz:
                self.term = u
                self.piece = game.pieces[u]
                self.process()
                ip = 1
        if ip == 0:
            print('This is not a valid piece\n')

    def process(self):
        self.valid = 1
        if game.gameover == 1 or game.gameover == 2:
            print('The game is already over!\n')
            self.valid = 0
            return
        if self.ox == self.nx and self.oy == self.ny and self.oz == self.nz:
            print('The two specified locations must be different\n')
            self.valid = 0
            return
        if not self.piece.atr['col'] == game.turn:
            print('This piece is not a valid colour\n')
            self.valid = 0
            return
        self.capture = 0
        for piecetwo in range(0, len(game.pieces)):
            if game.pieces[piecetwo].atr['pos'][0] == self.nx and game.pieces[piecetwo].atr['pos'][1] == self.ny and game.pieces[piecetwo].atr['pos'][2] == self.nz:
                if self.piece.atr['col'] == game.pieces[piecetwo].atr['col']:
                    print('You already have a piece here\n')
                    self.valid = 0
                    return
                else:
                    self.capture = 1
                    break
        if self.piece.atr['typ'] == 'king':
            if self.dx <= 1 and self.dy <= 1 and self.dz <= 1:
                pass
            elif self.dx == 2 and self.dy == 0 and self.dz == 0:
                self.rookpath()
                if self.valid == 1:
                    self.castlingvar = True
                    self.castling()
                    self.castlingvar = False
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'pawn':
            if self.capture == 1:
                if (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 1:
                    print('Pawns can only capture on sideways diagonals\n')
                    self.valid = 0
                elif (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dx == 1 and self.dl[0] == 0 and self.dl[1] == 1 and self.dl[2] == 1:
                    pass
                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 1 and self.dl[1] == 1 and self.dl[2] == 1:
                    pass
                else:
                    print('This is not a valid location\n')
                    self.valid = 0
            if self.capture == 0:
                if (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 1:
                    pass
                elif (self.ny - self.oy == game.turn*2 or self.nz - self.oz == game.turn*2) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 2:
                    if self.piece.atr['first'] == 0:
                        self.rookpath()
                        self.enpass2 = [int((self.ox+self.nx)/2), int((self.oy+self.ny)/2), int((self.oz+self.nz)/2)]
                    else:
                        print('Pawns can only double step on their first turn\n')
                        self.valid = 0
                elif (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dx == 1 and self.dl[0] == 0 and self.dl[1] == 1 and self.dl[2] == 1:
                    if game.enpass[0] == self.nx and game.enpass[1] == self.ny and game.enpass[2] == self.nz:
                        for piecetwo in range(0, len(game.pieces)):
                            if game.pieces[piecetwo].atr['moved_last_turn'] == True:
                                self.capture = 1
                                break
                    else:
                        print('Pawns can only move on sideways diagonals to capture\n')
                        self.valid = 0
                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 1 and self.dl[1] == 1 and self.dl[2] == 1:
                    if game.enpass[0] == self.nx and game.enpass[1] == self.ny and game.enpass[2] == self.nz:
                        for piecetwo in range(0, len(game.pieces)):
                            if game.pieces[piecetwo].atr['moved_last_turn'] == True:
                                self.capture = 1
                                break
                    else:
                        print('Pawns can only move on sideways diagonals to capture\n')
                        self.valid = 0
                else:
                    print('This is not a valid location\n')
                    self.valid = 0
        if self.piece.atr['typ'] == 'peasant':
            if self.capture == 1:
                if (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 1:
                    print('Peasants can only capture on three dimensional diagonals\n')
                    self.valid = 0
                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 1 and self.dl[2] == 1:
                    print('Peasants can only capture on three dimensional diagonals\n')
                    self.valid = 0
                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 1 and self.dl[1] == 1 and self.dl[2] == 1:
                    pass
                else:
                    print('This is not a valid location\n')
                    self.valid = 0
            if self.capture == 0:
                if (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 1:
                    pass
                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 1 and self.dl[2] == 1:
                    pass
                elif (self.ny - self.oy == game.turn*2 or self.nz - self.oz == game.turn*2) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 2:
                    if self.piece.atr['first'] == 0:
                        self.rookpath()
                        self.enpass2 = [int((self.ox+self.nx)/2), int((self.oy+self.ny)/2), int((self.oz+self.nz)/2)]
                    else:
                        print('Peasants can only double step on their first turn\n')
                        self.valid = 0
                elif (self.ny - self.oy == game.turn*2 and self.nz - self.oz == game.turn*2) and self.dl[0] == 0 and self.dl[1] == 2 and self.dl[2] == 2:
                    if self.piece.atr['first'] == 0:
                        self.bishoppath()
                        self.enpass2 = [int((self.ox+self.nx)/2), int((self.oy+self.ny)/2), int((self.oz+self.nz)/2)]
                    else:
                        print('Peasants can only double step on their first turn\n')
                        self.valid = 0
                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 1 and self.dl[1] == 1 and self.dl[2] == 1:
                    if game.enpass[0] == self.nx and game.enpass[1] == self.ny and game.enpass[2] == self.nz:
                        for piecetwo in range(0, len(game.pieces)):
                            if game.pieces[piecetwo].atr['moved_last_turn'] == True:
                                self.capture = 1
                                break
                    else:
                        print('Peasants can only move on three dimensional diagonals to capture\n')
                        self.valid = 0
                else:
                    print('This is not a valid location\n')
                    self.valid = 0
        if self.piece.atr['typ'] == 'soldier':
            if (self.dx <= 1 and self.dy <= 1 and self.dz <= 1):
                pass
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'knight':
            if self.dl[0] == 0 and self.dl[1] == 1 and self.dl[2] == 2:
                pass
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'horse':
            if self.dl[0] == 1 and self.dl[1] == 1 and self.dl[2] == 2:
                pass
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'elephant':
            if self.dl[0] == 1 and self.dl[1] == 2 and self.dl[2] == 2:
                pass
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'rook':
            if self.dl[0] == 0 and self.dl[1] == 0:
                self.rookpath()
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'bishop':
            if (self.dx == self.dy and self.dz == 0) or (self.dx == self.dz and self.dy == 0) or (self.dy == self.dz and self.dx == 0):
                self.bishoppath()
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'cardinal':
            if (self.dx == self.dy and self.dx == self.dz):
                self.cardinalpath()
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'queen':
            if self.dl[0] == 0 and self.dl[1] == 0:
                self.rookpath()
            elif (self.dx == self.dy and self.dz == 0) or (self.dx == self.dz and self.dy == 0) or (self.dy == self.dz and self.dx == 0):
                self.bishoppath()
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'duchess':
            if self.dl[0] == 0 and self.dl[1] == 0:
                self.rookpath()
            elif (self.dx == self.dy and self.dx == self.dz):
                self.cardinalpath()
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'princess':
            if (self.dx == self.dy and self.dz == 0) or (self.dx == self.dz and self.dy == 0) or (self.dy == self.dz and self.dx == 0):
                self.bishoppath()
            elif (self.dx == self.dy and self.dx == self.dz):
                self.cardinalpath()
            else:
                print('This is not a valid location\n')
                self.valid = 0
        if self.piece.atr['typ'] == 'pope':
            if self.dl[0] == 0 and self.dl[1] == 0:
                self.rookpath()
            elif (self.dx == self.dy and self.dz == 0) or (self.dx == self.dz and self.dy == 0) or (self.dy == self.dz and self.dx == 0):
                self.bishoppath()
            elif (self.dx == self.dy and self.dx == self.dz):
                self.cardinalpath()
            else:
                print('This is not a valid location\n')
                self.valid = 0

        if self.valid == 1:
            if self.capture == 1:
                move2 = movement()
                move2.piece = game.pieces[piecetwo]
                move2.term = piecetwo
                if move2.piece.atr['col'] == 1:
                    game.capturedposg = game.capturedposw
                if move2.piece.atr['col'] == -1:
                    game.capturedposg = game.capturedposb
                move2.nx = game.capturedposg%8 + 1
                if move2.piece.atr['col'] == 1:
                    move2.ny = -((game.capturedposg//8)%4)+8
                if move2.piece.atr['col'] == -1:
                    move2.ny = ((game.capturedposg//8)%4)+1
                move2.nz = -(game.capturedposg//32)-1
                if move2.piece.atr['col'] == 1:
                    game.capturedposw = game.capturedposw + 1
                    game.write(f'{home}/public/misc.txt',None,str(game.capturedposw),1)
                    capturer = ('black')
                    captured = ('white')
                if move2.piece.atr['col'] == -1:
                    game.capturedposb = game.capturedposb + 1
                    game.write(f'{home}/public/misc.txt',None,str(game.capturedposb),2)
                    capturer = ('white')
                    captured = ('black')
                print(f'A {captured} {game.pieces[piecetwo].atr["typ"]} has been captured!\n')
                move2.update()
                game.write(f'{home}/public/pieces.txt',None,f'[{move2.piece.atr["typ"]},({move2.piece.atr["pos"][0]},{move2.piece.atr["pos"][1]},{move2.piece.atr["pos"][2]}),{move2.piece.atr["col"]},{move2.piece.atr["first"]},{move2.piece.atr["moved_last_turn"]}]',move2.term)

                if game.pieces[piecetwo].atr['typ'] == 'king':
                    print(f'Game over, {capturer} wins!!')
                    game.gameover = 2
                    game.write(f'{home}/public/misc.txt',None,str(game.gameover),5)
                    print('Do you want to play again? (y/n)')

            if self.piece.atr['typ'] == 'pawn' or self.piece.atr['typ'] == 'peasant':
                if self.ny == 4+game.turn*4 and self.nz == 4+game.turn*4:
                    self.pro()
            self.update()

            if move.castlingvar == False:
                if game.turn == 1:
                    game.turn = -1
                    print('Black\'s turn\n')
                elif game.turn == -1:
                    game.turn = 1
                    print('White\'s turn\n')
                for u in range(0,len(game.pieces)):
                    if game.pieces[u].atr['moved_last_turn'] == True:
                        game.pieces[u].atr['moved_last_turn'] = False
                        game.write(f'{home}/public/pieces.txt',None,f'[{game.pieces[u].atr["typ"]},({game.pieces[u].atr["pos"][0]},{game.pieces[u].atr["pos"][1]},{game.pieces[u].atr["pos"][2]}),{game.pieces[u].atr["col"]},{game.pieces[u].atr["first"]},{game.pieces[u].atr["moved_last_turn"]}]',u)
                        app.rendersi(game.pieces[u].atr,'piece')
                move.piece.atr['moved_last_turn'] = True
                game.write(f'{home}/public/pieces.txt',None,f'[{self.piece.atr["typ"]},({self.piece.atr["pos"][0]},{self.piece.atr["pos"][1]},{self.piece.atr["pos"][2]}),{self.piece.atr["col"]},{self.piece.atr["first"]},{self.piece.atr["moved_last_turn"]}]',self.term)
                try:
                    move.move3.piece.atr['moved_last_turn'] = True
                    game.write(f'{home}/public/pieces.txt',None,f'[{move.move3.piece.atr["typ"]},({move.move3.piece.atr["pos"][0]},{move.move3.piece.atr["pos"][1]},{move.move3.piece.atr["pos"][2]}),{move.move3.piece.atr["col"]},{move.move3.piece.atr["first"]},{move.move3.piece.atr["moved_last_turn"]}]',move.move3.term)
                    app.rendersi(move.move3.piece.atr,'piece')
                except:
                    pass
                app.rendersi(self.piece.atr,'piece')
                game.write(f'{home}/public/misc.txt',None,str(game.turn),0)
                game.moved_from_last_turn = [self.ox,self.oy,self.oz]
                game.write(f'{home}/public/misc.txt','moved_from_last_turn: ',f'({game.moved_from_last_turn[0]},{game.moved_from_last_turn[1]},{game.moved_from_last_turn[2]})',3)
                game.enpass = self.enpass2
                game.write(f'{home}/public/misc.txt','enpass: ',f'({game.enpass[0]},{game.enpass[1]},{game.enpass[2]})',4)
                move.move3 = None

    def castling(self):
        if self.nx-self.ox == 2:
            castle = app.board[self.oy-1][self.oz-1][self.ox+2]
        if self.nx-self.ox == -2:
            castle = app.board[self.oy-1][self.oz-1][self.ox-5]
        if not 'rel' in (castle.atr.keys()):
            print('There is no valid rook to castle with\n')
            self.valid = 0
            return
        if self.capture == 1:
            print('You can not capture pieces while castling\n')
            self.valid = 0
            return
        if self.piece.atr['first'] == 1 or castle.atr['rel'].atr['first'] == 1:
            print('You have already moved either your king or your rook\n')
            self.valid = 0
            return
        move.move3 = movement()
        move.move3.ox = castle.atr['pos'][0]
        move.move3.oy = castle.atr['pos'][1]
        move.move3.oz = castle.atr['pos'][2]
        move.move3.nx = int(move.ox-(move.ox - move.nx)/2)
        move.move3.ny = move.oy
        move.move3.nz = move.oz
        move.move3.findpiece()

    def pro(self):
        while True:
            print(f'Please enter a piece to promote the {self.piece.atr["typ"]} into')
            prop = input()
            print('')
            if prop == 'knight' or prop == 'horse' or prop == 'elephant' or prop == 'rook' or prop == 'bishop' or prop == 'cardinal' or prop == 'queen' or prop == 'duchess' or prop == 'princess' or prop == 'pope':
                self.piece.atr['typ'] = prop
            else:
                print('This is not a valid piece\n')

    def rookpath(self):
        if self.dx != 0:
            d = 0
            da = [self.ox-1,self.nx-1]
            de = [0,self.piece.atr['pos'][1]-1,self.piece.atr['pos'][2]-1]
        if self.dy != 0:
            d = 1
            da = [self.oy-1,self.ny-1]
            de = [self.piece.atr['pos'][0]-1,0,self.piece.atr['pos'][2]-1]
        if self.dz != 0:
            d = 2
            da = [self.oz-1,self.nz-1]
            de = [self.piece.atr['pos'][0]-1,self.piece.atr['pos'][1]-1,0]
        if (da[0] - da[1]) > 0:
            pos1 = -1
        else:
            pos1 = 1
        for u in range(1,self.dl[2]):
            de[d] = u*pos1 + da[0]
            if 'rel' in (app.board[de[1]][de[2]][de[0]].atr.keys()):
                print(f'You can not move {self.piece.atr["typ"]}s through other pieces\n')
                self.valid = 0
                return

    def bishoppath(self):
        if self.dx == 0:
            d = [1,2]
            da = [self.oy-1,self.ny-1]
            db = [self.oz-1,self.nz-1]
            de = [self.piece.atr['pos'][0]-1,0,0]
        if self.dy == 0:
            d = [0,2]
            da = [self.ox-1,self.nx-1]
            db = [self.oz-1,self.nz-1]
            de = [0,self.piece.atr['pos'][1]-1,0]
        if self.dz == 0:
            d = [0,1]
            da = [self.ox-1,self.nx-1]
            db = [self.oy-1,self.ny-1]
            de = [0,0,self.piece.atr['pos'][2]-1]
        if (da[0] - da[1]) > 0:
            pos1 = -1
        else:
            pos1 = 1
        if (db[0] - db[1]) > 0:
            pos2 = -1
        else:
            pos2 = 1
        for u in range (1,self.dl[2]):
            de[d[0]] = u*pos1 + da[0]
            de[d[1]] = u*pos2 + db[0]
            if 'rel' in (app.board[de[1]][de[2]][de[0]].atr.keys()):
                print(f'You can not move {self.piece.atr["typ"]}s through other pieces\n')
                self.valid = 0
                return

    def cardinalpath(self):
        if (self.ox-self.nx) > 0:
            pos1 = -1
        else:
            pos1 = 1
        if (self.oy-self.ny) > 0:
            pos2 = -1
        else:
            pos2 = 1
        if (self.oz-self.nz) > 0:
            pos3 = -1
        else:
            pos3 = 1
        for u in range (1,self.dl[2]):
            de = [u*pos1+self.ox-1,u*pos2+self.oy-1,u*pos3+self.oz-1]
            if 'rel' in (app.board[de[1]][de[2]][de[0]].atr.keys()):
                print(f'You can not move {self.piece.atr["typ"]}s through other pieces\n')
                self.valid = 0
                return

    def update(self):
        self.piece.atr['pos'][0] = self.nx
        self.piece.atr['pos'][1] = self.ny
        self.piece.atr['pos'][2] = self.nz
        del self.piece.atr['rel'].atr['rel']
        del self.piece.atr['rel']
        app.reunrenders(self.piece)
        app.rerenders(self.piece)
        if move.castlingvar == False:
            if not None in game.moved_from_last_turn:
                app.board[game.moved_from_last_turn[1]-1][game.moved_from_last_turn[2]-1][game.moved_from_last_turn[0]-1].atr['obj'].setTexture(app.board[game.moved_from_last_turn[1]-1][game.moved_from_last_turn[2]-1][game.moved_from_last_turn[0]-1].atr['col'])
            app.board[self.oy-1][self.oz-1][self.ox-1].atr['obj'].setTexture(app.colour[3][2][1])
        self.piece.atr['first'] = 1

##

home = "../3dchess"

while True:
    print('Load from a saved file? (y/n)')
    savefile = input()
    print('')
    if savefile == 'y':
        game.open()
        break
    elif savefile == 'n':
        game.restart()
        break
    else:
        print('This is not a valid selection\n')

read = read()
move = movement()
move.move3 = None



## Panda3d task
#Change name to render
app = rendering_task(move, game)
app.start()

read.stuff()
