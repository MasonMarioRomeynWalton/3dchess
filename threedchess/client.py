#!/usr/bin/python3
import socket
import json

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

import threading
import os
import sys
import traceback
import time
from math import *

import lib.cameras as cameras

##

def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    print('Press any key to exit.')
    input()
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

##

def receives():
    while True:
        try:
            z = read.receivess
            del read.receivess
            return(z)
        except:
            pass
        time.sleep(0.01)

def close():
    try:
        s.close()
    except:
        pass
    print('You have lost connection with the server')
    print('Press any key to close\n')
    input()
    exit()

##

s = socket.socket()
port = 1599

while True:
    print('Please input the name of the server you wish to connect to')
    server_name = input()
    print('')
    try:
        s.connect((server_name, port))
        break
    except:
        print(f'Unable to connect to server "{server_name}"')
    time.sleep(0.01)
try:
    s.send(json.dumps('3dchess').encode('UTF-8'))
    (s.recv(1024)).decode('UTF-8')
except:
    close()

##

class piecec:
    def __init__(self,typ,pos,col,moved_last_turn):
        self.atr = {'typ':typ,'pos':pos,'col':col,'first':0,'moved_last_turn':moved_last_turn,'ispicked1':False,'ispicked2':False}

class boardc:
    def __init__(self,pos,col):
        self.atr = {'pos':pos,'col':col,'moved_last_turn':False,'ispicked1':False,'ispicked2':False}

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
        print('"c" to teleport to your start')
        print('"v" to teleport to your opponent\'s start')
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

        pieceslength = receives()
        self.pieces = []
        for u in range(0,pieceslength):
            self.pieces.append(piecec(receives(),receives(),receives(),receives()))

        self.capturedposw = receives()
        self.capturedposb = receives()
        self.moved_from_last_turn = [receives(),receives(),receives()]

    def __init__(self):
        self.s = 5
        self.hs = self.s/2
        self.fs = self.s*4.5

game = game()

class read():
    def stuff(self):
        while True:
            print('Enter:')
            print('"h" for help')
            print('"r" to restart')
            print('Or enter your move')
            h = input()
            print('')
            if h == 'help' or h == 'help!':
                self.helpmenu()
                continue
            if h == 'h':
                self.hellpmenu()
                continue
            if h == 'r':
                read.sendx.append(['r',None])
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
                self.com = list(h)
                self.sendx.append(['m',self.com])
                self.continuem = 0
                while True:
                    if self.continuem == 1:
                        break
                    time.sleep(0.01)
                self.com[0] = '0'
                self.com[1] = '0'
                self.com[2] = '0'
                self.com[4] = '0'
                self.com[5] = '0'
                self.com[6] = '0'

    def helpmenu(self):
        print('''When I was younger so much younger than today\nI never needed anybody's help in any way\nBut now these days are gone, I'm not so self assured\nNow I find I've changed my mind and opened up the doors\nUh... You wanted a menu that helps gameplay? Nevermind this then. Press "h" to acess the other help menu''')

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

    def receivingthread(self):
        while True:
            if len(self.sendx) != 0:
                try:
                    s.send(json.dumps(self.sendx[0]).encode('UTF-8'))
                    (s.recv(1024)).decode('UTF-8')
                except:
                    close()
                del self.sendx[0]
            try:
                s.setblocking(0)
                s.settimeout(0.001)
                self.command = (json.loads((s.recv(1024)).decode('UTF-8')))
                s.send(' '.encode('UTF-8'))
            except Exception as e:
                if not str(e) == 'timed out':
                    close()
                s.setblocking(1)
                continue
            s.setblocking(1)
            self.valid = 0
            if self.command[0] == 's':
                self.receivess = self.command[1]
            elif self.command[0] == 't':
                self.receivest = self.command[1]
                print(self.receivest[0])
            elif self.command[0] == 'h':
                self.receivesh = self.command[1]
                self.term = self.receivesh[0]
                game.pieces[self.term].atr['moved_last_turn'] = self.receivesh[1]
                app.rendersi(game.pieces[self.term].atr,'piece')
            elif self.command[0] == 'f':
                self.receivesf = self.command[1]
                print(self.receivesf[0])
                self.continuem = 1
            elif self.command[0] == 'm':
                self.receivesm = self.command[1]
                self.term = self.receivesm[0]
                game.pieces[self.term].atr['typ'] = self.receivesm[1]
                game.pieces[self.term].atr['pos'] = self.receivesm[2]
                game.pieces[self.term].atr['moved_last_turn'] = self.receivesm[3]
                self.castlingvar = self.receivesm[5]
                if self.castlingvar == False:
                    if not None in game.moved_from_last_turn:
                        app.board[game.moved_from_last_turn[1]-1][game.moved_from_last_turn[2]-1][game.moved_from_last_turn[0]-1].atr['obj'].setTexture(app.board[game.moved_from_last_turn[1]-1][game.moved_from_last_turn[2]-1][game.moved_from_last_turn[0]-1].atr['col'])
                game.moved_from_last_turn = self.receivesm[4]
                if self.castlingvar == False:
#                    print(app.board)
#                    print(app.colour[3][2][1])
                    print(game.moved_from_last_turn)
                    app.board[game.moved_from_last_turn[1]-1][game.moved_from_last_turn[2]-1][game.moved_from_last_turn[0]-1].atr['obj'].setTexture(app.colour[3][2][1])
                del game.pieces[self.term].atr['rel'].atr['rel']
                del game.pieces[self.term].atr['rel']
                app.reunrenders(game.pieces[self.term])
                app.rerenders(game.pieces[self.term])
                self.valid = 1
                self.continuem = 1
            elif self.command[0] == 'r':
                self.restartthread = threading.Thread(target = self.restartthread)
                self.restartthread.start()
            time.sleep(0.001)

    def restartthread(self):
        player = receives()
        if player == 1:
            player = 1
            print('You are playing white\n')
        elif player == -1:
            player = -1
            print('You are playing black\n')
        app.reset()
        app.reset2()
        self.com[0] = '0'
        self.com[1] = '0'
        self.com[2] = '0'
        self.com[4] = '0'
        self.com[5] = '0'
        self.com[6] = '0'
        app.unrenders()
        app.unrendersboard()
        game.restart()
        app.rendersboard()
        app.renders()
        print('Enter:')
        print('"h" for help')
        print('"r" to restart')
        print('Or enter your move')

    def __init__(self):
        self.sendx = []
        self.continuem = 0
        self.com = [0]*7

class MyApp(ShowBase):
    def renders(self):
        self.step = False
        for u in range(0,len(game.pieces)):
            game.pieces[u].atr['obj'] = loader.loadModel(f'''{game.pieces[u].atr['typ']}.dae''')
            game.pieces[u].atr['obj'].reparentTo(render)
            game.pieces[u].atr['obj'].setPos(game.pieces[u].atr['pos'][1]*game.s,game.pieces[u].atr['pos'][2]*game.s,game.pieces[u].atr['pos'][0]*game.s)
            game.pieces[u].atr['obj'].setScale(game.hs,game.hs,game.hs)
            if game.pieces[u].atr['col'] == 1:
                game.pieces[u].atr['obj'].setTexture(self.colour[0][0],1)
                game.pieces[u].atr['obj'].setHpr(0,0,180)
            if game.pieces[u].atr['col'] == -1:
                game.pieces[u].atr['obj'].setTexture(self.colour[0][1],1)
                game.pieces[u].atr['obj'].setHpr(0,0,0)
            game.pieces[u].atr['obj'].setPythonTag('piece',game.pieces[u].atr)
            if game.pieces[u].atr['pos'][2]-1 >= 0:
                game.pieces[u].atr['rel'] = self.board[game.pieces[u].atr['pos'][1]-1][game.pieces[u].atr['pos'][2]-1][game.pieces[u].atr['pos'][0]-1]
                self.board[game.pieces[u].atr['pos'][1]-1][game.pieces[u].atr['pos'][2]-1][game.pieces[u].atr['pos'][0]-1].atr['rel'] = game.pieces[u]
            if game.pieces[u].atr['moved_last_turn'] == True:
                self.rendersi(game.pieces[u].atr,'piece')
        if not None in game.moved_from_last_turn:
            self.board[game.moved_from_last_turn[1]-1][game.moved_from_last_turn[2]-1][game.moved_from_last_turn[0]-1].atr['obj'].setTexture(self.colour[3][2][1])
        self.step = True

    def unrenders(self):
        self.step = False
        for u in range(0,len(game.pieces)):
            game.pieces[u].atr['obj'].removeNode()
            time.sleep(0.01)
            loader.unloadModel(f'''{game.pieces[u].atr['typ']}.dae''')
        self.step = True

    def rendersboard(self):
        self.step = False
        self.board = []
        for boardx in range (0,8):
            self.board.append([])
            for boardy in range (0,8):
                self.board[boardx].append([])
                for boardz in range (0,8):
                    self.board[boardx][boardy].append(boardc([boardz+1,boardx+1,boardy+1],self.colour[2][boardx%2][boardy%2][boardz%2]))
                    self.board[boardx][boardy][boardz].atr['obj'] = loader.loadModel('board2.dae')
                    self.board[boardx][boardy][boardz].atr['obj'].reparentTo(render)
                    self.board[boardx][boardy][boardz].atr['obj'].setPos(boardx*game.s+game.s,boardy*game.s+0.01+0.5*game.s,boardz*game.s+game.s)
                    self.board[boardx][boardy][boardz].atr['obj'].setScale(game.hs,game.hs,game.hs)
                    self.board[boardx][boardy][boardz].atr['obj'].setTexture(self.board[boardx][boardy][boardz].atr['col'])
                    self.board[boardx][boardy][boardz].atr['obj'].setPythonTag('board',self.board[boardx][boardy][boardz].atr)
        self.step = True

    def unrendersboard(self):
        self.step = False
        for boardx in range(0,8):
            for boardy in range(0,8):
                for boardz in range(0,8):
                    self.board[boardx][boardy][boardz].atr['obj'].removeNode()
                    time.sleep(0.01)
        self.step = True

    def rerenders(self,piece):
        self.step = False
        piece.atr['obj'] = loader.loadModel(f'''{piece.atr['typ']}.dae''')
        piece.atr['obj'].reparentTo(render)
        piece.atr['obj'].setPos(piece.atr['pos'][1]*game.s,piece.atr['pos'][2]*game.s,piece.atr['pos'][0]*game.s)
        piece.atr['obj'].setScale(game.hs,game.hs,game.hs)
        if piece.atr['col'] == 1:
            piece.atr['obj'].setTexture(self.colour[0][0], 1)
            piece.atr['obj'].setHpr(0,0,180)
        if piece.atr['col'] == -1:
            piece.atr['obj'].setTexture(self.colour[0][1], 1)
            piece.atr['obj'].setHpr(0,0,0)
        piece.atr['obj'].setPythonTag('piece',piece.atr)
        if piece.atr['pos'][2]-1 >= 0:
            piece.atr['rel'] = self.board[piece.atr['pos'][1]-1][piece.atr['pos'][2]-1][piece.atr['pos'][0]-1]
            self.board[piece.atr['pos'][1]-1][piece.atr['pos'][2]-1][piece.atr['pos'][0]-1].atr['rel'] = piece
        self.step = True
        self.rendersi(piece.atr,'piece')

    def reunrenders(self,piece):
        self.step = False
        piece.atr['obj'].removeNode()
        time.sleep(0.01)
        loader.unloadModel(f'''{piece.atr['typ']}.dae''')
        self.step = True

    def rendersi(self,highlightpiece,piecetype):
        if highlightpiece['ispicked2'] == True:
            if piecetype == 'piece':
                if highlightpiece['col'] == 1:
                    color = self.colour[3][1][0]
                if highlightpiece['col'] == -1:
                    color = self.colour[3][1][2]
            if piecetype == 'board':
                color = self.colour[3][1][1]
        if highlightpiece['moved_last_turn'] == True:
            if highlightpiece['col'] == 1:
                color = self.colour[3][2][0]
            if highlightpiece['col'] == -1:
                color = self.colour[3][2][2]
        if highlightpiece['ispicked1'] == True:
            if highlightpiece['col'] == 1:
                color = self.colour[3][0][0]
            if highlightpiece['col'] == -1:
                color = self.colour[3][0][1]
        if highlightpiece['ispicked1'] == False and highlightpiece['ispicked2'] == False and highlightpiece['moved_last_turn'] == False:
            if highlightpiece['col'] == 1:
                color = self.colour[0][0]
            elif highlightpiece['col'] == -1:
                color = self.colour[0][1]
            elif not None in game.moved_from_last_turn:
                if highlightpiece == self.board[game.moved_from_last_turn[1]-1][game.moved_from_last_turn[2]-1][game.moved_from_last_turn[0]-1].atr:
                    color = self.colour[3][2][1]
                else:
                    color = highlightpiece['col']
            else:
                color = highlightpiece['col']
        highlightpiece['obj'].setTexture(color)

    def click(self):
        read.com[0] = '0'
        read.com[1] = '0'
        read.com[2] = '0'
        self.reset()
        try:
            mpos = base.mouseWatcherNode.getMouse()
        except:
            print('You clicked off the screen\n')
            return
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        self.myTraverser.traverse(render)
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            pickedObj = self.queue.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetPythonTag('piece')
            self.pickedObjp = pickedObj.getNetPythonTag('piece')
            if self.pickedObjp != None:
                self.pickedObjp['ispicked1'] = True
                self.rendersi(self.pickedObjp,'piece')
                read.com[0] = str(self.pickedObjp['pos'][0])
                read.com[1] = str(self.pickedObjp['pos'][1])
                read.com[2] = str(self.pickedObjp['pos'][2])

    def click2(self):
        read.com[4] = '0'
        read.com[5] = '0'
        read.com[6] = '0'
        self.reset2()
        try:
            mpos = base.mouseWatcherNode.getMouse()
        except:
            print('You clicked off the screen\n')
            return
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        self.myTraverser.traverse(render)
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            pickedObj = self.queue.getEntry(0).getIntoNodePath()
            self.pickedObjc = pickedObj.getNetPythonTag('piece')
            self.pickedObjb = pickedObj.getNetPythonTag('board')
            if self.pickedObjb != None or self.pickedObjc != None:
                if self.pickedObjb != None:
                    if 'rel' in self.pickedObjb.keys() != None:
                        self.pickedObjc = self.pickedObjb['rel'].atr
                        self.pickedObjc['ispicked2'] = True
                        self.rendersi(self.pickedObjc,'piece')
                    self.pickedObjb['ispicked2'] = True
                    self.rendersi(self.pickedObjb,'board')
                elif self.pickedObjc != None:
                    if 'rel' in self.pickedObjc.keys() != None:
                        self.pickedObjb = self.pickedObjc['rel'].atr
                        self.pickedObjb['ispicked2'] = True
                        self.rendersi(self.pickedObjb,'board')
                    self.pickedObjc['ispicked2'] = True
                    self.rendersi(self.pickedObjc,'piece')
                if self.pickedObjb != None:
                    read.com[4] = str(self.pickedObjb['pos'][0])
                    read.com[5] = str(self.pickedObjb['pos'][1])
                    read.com[6] = str(self.pickedObjb['pos'][2])
                else:
                    read.com[4] = str(self.pickedObjc['pos'][0])
                    read.com[5] = str(self.pickedObjc['pos'][1])
                    read.com[6] = str(self.pickedObjc['pos'][2])

    def stuff2(self):
        self.reset2()

        read.sendx.append(['v',read.com])
        read.continuem = 0
        while True:
            if read.continuem == 1:
                break
            time.sleep(0.01)
        read.com[4] = '0'
        read.com[5] = '0'
        read.com[6] = '0'
        if hasattr(read,'valid'):
            if read.valid == 1:
                self.reset()
                read.com[0] = '0'
                read.com[1] = '0'
                read.com[2] = '0'

    def reset(self):
        if hasattr(self,'pickedObjp'):
            if self.pickedObjp != None:
                self.pickedObjp['ispicked1'] = False
                self.rendersi(self.pickedObjp,'piece')
                del self.pickedObjp

    def reset2(self):
        if hasattr(self,'pickedObjc'):
            if self.pickedObjc != None:
                self.pickedObjc['ispicked2'] = False
                self.rendersi(self.pickedObjc,'piece')
                del self.pickedObjc
        if hasattr(self,'pickedObjb'):
            if self.pickedObjb != None:
                self.pickedObjb['ispicked2'] = False
                self.rendersi(self.pickedObjb,'piece')
                del self.pickedObjb

    def __init__(self):
        self.nout = MultiplexStream()
        Notify.ptr().setOstreamPtr(self.nout, 0)
        self.nout.addFile(Filename("panda3doutput.txt"))
        ShowBase.__init__(self)
        render.setShaderAuto()
        self.disableMouse()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.myTraverser = CollisionTraverser('traverser name')
        self.queue = CollisionHandlerQueue()
        self.myTraverser.addCollider(self.pickerNP,self.queue)

        self.colourl2 = {}
        self.directionalLight = [[45,0,0],[135,0,0],[45,180,0],[135,180,0],[45,30,0],[45,-30,0],[135,30,0],[135,-30,0],[45,150,0],[45,-150,0],[135,150,0],[135,-150,0]]
        self.directionalLights = []
        self.directionalLightNP= []
        self.boards = []
        self.post = [[4,4],[4,-4],[-4,4],[-4,-4]]
        self.posts = []

        self.colourl = ['white','black','grid','grid2','brown','darkblue','lightmono','lightred','lightyellow','darkyellow','darkred','darkmono','lightblue','highlightw','highlightb','capturew','captureg','captureb','lastw','lastg','lastb']

        for u in range(0,len(self.colourl)):
            self.colourl2[f'{self.colourl[u]}'] = loader.loadTexture(f'{home}/static/maps/{self.colourl[u]}.png')
            self.colourl2[f'{self.colourl[u]}'].setMagfilter(SamplerState.FT_nearest)

        self.colour = [[self.colourl2['white'],self.colourl2['black']],[[self.colourl2['grid'],self.colourl2['grid2']],self.colourl2['brown']],[[[self.colourl2['darkblue'],self.colourl2['lightmono']],[self.colourl2['lightyellow'],self.colourl2['darkred']]],[[self.colourl2['lightred'],self.colourl2['darkyellow']],[self.colourl2['darkmono'],self.colourl2['lightblue']]]],[[self.colourl2['highlightw'],self.colourl2['highlightb']],[self.colourl2['capturew'],self.colourl2['captureg'],self.colourl2['captureb']],[self.colourl2['lastw'],self.colourl2['lastg'],self.colourl2['lastb']]]]

        for u in range(0,12):
            self.directionalLights.append(DirectionalLight('directionalLight'))
            self.directionalLights[u].setColor((0.3, 0.3, 0.3, 1))
            self.directionalLightNP.append(render.attachNewNode(self.directionalLights[u]))
            self.directionalLightNP[u].setHpr(self.directionalLight[u][0],self.directionalLight[u][1],self.directionalLight[u][2])
            render.setLight(self.directionalLightNP[u])

        self.rendersboard()

        for u in range(0,8):
            self.boards.append(loader.loadModel('board.dae'))
            self.boards[u].reparentTo(render)
            self.boards[u].setPos(game.fs,(u+0.5)*game.s,game.fs)
            self.boards[u].setScale(game.hs,game.hs,game.hs)
            self.boards[u].setHpr(0,0,90)
            self.boards[u].setTexture(self.colour[1][0][u%2])

        for u in range(0,4):
            self.posts.append(loader.loadModel('post.dae'))
            self.posts[u].reparentTo(render)
            self.posts[u].setPos(game.fs+self.post[u][0]*game.s,game.s*4,game.fs+self.post[u][1]*game.s)
            self.posts[u].setScale(game.hs,game.hs,game.hs)
            self.posts[u].setTexture(self.colour[1][1])

        self.renders()

##

home = "../3dchess"

read = read()
receivingthread = threading.Thread(target = read.receivingthread)
receivingthread.start()

connect_number = receives()

if connect_number == 1:
    print('Load from a saved file? (y/n)')
    while True:
        savefile = input()
        if savefile == 'y':
            read.sendx.append(['s',savefile])
            print('Please enter the colour you wish to continue as')
            while True:
                player = input()
                if player == 'white' or player == 'White':
                    player = 1
                    break
                elif player == 'black' or player == 'Black':
                    player = -1
                    break
                else:
                    print('This is not a valid selection')
            read.sendx.append(['s',player])
            break
        if savefile == 'n':
            read.sendx.append(['s',savefile])
            player = receives()
            if player == 1:
                player = 1
                print('You are playing white\n')
            elif player == -1:
                player = -1
                print('You are playing black\n')
            break
        else:
            print('This is not a valid selection')

elif connect_number == 2:
    print('Your opponent is selecting save file')
    savefile = receives()
    if savefile == 'y':
        print('Your opponent has selected an existing save')
        print('Your opponent is selecting their colour')
    if savefile == 'n':
        print('Your opponent has selected a new save')
        print('Your colour is being randomly generated')
    player = receives()
    if player == 1:
        player = -1
        print('You are playing black\n')
    elif player == -1:
        player = 1
        print('You are playing white\n')
game.restart()


app = MyApp()

## Our terminal thread

inputthread = threading.Thread(target = read.stuff)
inputthread.start()


## Panda3d task

camera = cameras.camera(game.s,game.fs)

if player == 1:
    camera.init_white()
if player == -1:
    camera.init_black()

movement_keylist = ['space','z','w','a','s','d','i','j','k','l']
hotkey_keylist = ['c','v','mouse1','mouse3','enter']
keymap = {key:0 for key in movement_keylist+hotkey_keylist}

def setKey(key, value):
    keymap[key] = value

for key in keymap.keys():
    if key in movement_keylist:
        base.accept(key, setKey, [key,1])
        base.accept(f'{key}-up', setKey, [key,0])
    if key in hotkey_keylist:
        base.accept(key, setKey, [key,1])

time_elapsed = 0
def check_for_input(camera, task):
    global time_elapsed
    movement_distance = time_elapsed*20
    rotation_distance = time_elapsed*14

    if (keymap['space']!=0):
        camera.move_up(movement_distance)

    if (keymap['z']!=0):
        camera.move_down(movement_distance)

    if (keymap['w']!=0):
        camera.move_forward(movement_distance)

    if (keymap['a']!=0):
        camera.move_left(movement_distance)

    if (keymap['s']!=0):
        camera.move_back(movement_distance)

    if (keymap['d']!=0):
        camera.move_right(movement_distance)

    if (keymap['i']!=0):
        camera.pitch_up(rotation_distance)

    if (keymap['k']!=0):
        camera.pitch_down(rotation_distance)

    if (keymap['j']!=0):
        camera.yaw_right(rotation_distance)

    if (keymap['l']!=0):
        camera.yaw_left(rotation_distance)

    if (keymap['c']!=0):
        camera.init_white()
        setKey('c',0)

    if (keymap['v']!=0):
        camera.init_black()
        setKey('v',0)

    if (keymap['mouse1']!=0):
        app.click()
        setKey('mouse1',0)

    if (keymap['mouse3']!=0):
        app.click2()
        setKey('mouse3',0)

    if (keymap['enter']!=0):
        app.stuff2()
        setKey('enter',0)

    time_elapsed = task.time - camera.time_at_last_update
    camera.update_camera()
        
    camera.time_at_last_update = task.time
    return task.cont

taskMgr.add(check_for_input, 'cameramove', extraArgs=[camera], appendTask=True)


while True:
    if app.step == True:
        taskMgr.step()
    time.sleep(0.01)
