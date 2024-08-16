from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

import threading
import time

from . import controlable_camera

home = "../../3dchess"

class rendering_task(threading.Thread):
    def __init__(self, move, game):
        threading.Thread.__init__(self)


        ## The game object
        self.game = game

        ## How big the game board is
        self.game_size = 5

        ## Half of the game board size
        self.half_game_size = self.game_size/2

        ## Multiplier of the game board size
        self.multiplied_game_size = self.game_size*4.5

        #To merge
        self.move = move
        self.init()

        ## Create the camera 
        self.camera = controlable_camera(self.game_size,self.multiplied_game_size)
        self.camera.init_white()

        ## Set the amount of time since the last camera update to 0
        self.time_elapsed = 0

        ## Create map of movement controls
        self.controls = [
            movement_control('space',  self.camera.move_up,       "move"  ),
            movement_control('z',      self.camera.move_down,     "move"  ),
            movement_control('w',      self.camera.move_forward,  "move"  ),
            movement_control('a',      self.camera.move_left,     "move"  ),
            movement_control('s',      self.camera.move_backward, "move"  ),
            movement_control('d',      self.camera.move_right,    "move"  ),
            movement_control('i',      self.camera.tilt_up,       "rotate"),
            movement_control('k',      self.camera.tilt_down,     "rotate"),
            movement_control('l',      self.camera.pan_right,     "rotate"),
            movement_control('j',      self.camera.pan_left,      "rotate"),

            hotkey_control(  'c',      self.camera.init_white),
            hotkey_control(  'v',      self.camera.init_black),
            hotkey_control(  'mouse1', self.click),
            hotkey_control(  'mouse3', self.click2),
            hotkey_control(  'enter',  self.stuff2)
        ]

    def run(self):
        # self.base = ShowBase()
        self.app = MyApp(game)


        self.start()


    def start(self):

        taskMgr.add(self.check_for_input, 'cameramove', extraArgs=[self.camera], appendTask=True)

        while True:
            if self.step == True:
                taskMgr.step()
            time.sleep(0.01)

    def check_for_input(self, camera, task):
        movement_distance = self.time_elapsed*20
        rotation_distance = self.time_elapsed*14

        for control in self.controls:
            if control.pressed == 1:
                if type(control) == movement_control:
                    if control.movement_type == "move":
                        control.key_press(movement_distance)
                    if control.movement_type == "rotate":
                        control.key_press(rotation_distance)
                if type(control) == hotkey_control:
                    control.key_press()

        self.time_elapsed = task.time - self.camera.time_at_last_update
        self.camera.update_camera()
        self.camera.time_at_last_update = task.time

        return task.cont

    def renders(self):
        self.step = False
        for u in range (0,len(self.game.pieces)):
            self.game.pieces[u].atr['obj'] = loader.loadModel(f'{self.game.pieces[u].atr["typ"]}.dae')
            self.game.pieces[u].atr['obj'].reparentTo(render)
            self.game.pieces[u].atr['obj'].setPos(self.game.pieces[u].atr['pos'][1]*self.game_size,self.game.pieces[u].atr['pos'][2]*self.game_size,self.game.pieces[u].atr['pos'][0]*self.game_size)
            self.game.pieces[u].atr['obj'].setScale(self.half_game_size,self.half_game_size,self.half_game_size)
            if self.game.pieces[u].atr['col'] == 1:
                self.game.pieces[u].atr['obj'].setTexture(self.colour[0][0], 1)
                self.game.pieces[u].atr['obj'].setHpr(0,0,180)
            if self.game.pieces[u].atr['col'] == -1:
                self.game.pieces[u].atr['obj'].setTexture(self.colour[0][1], 1)
                self.game.pieces[u].atr['obj'].setHpr(0,0,0)
            self.game.pieces[u].atr['obj'].setPythonTag('piece',self.game.pieces[u].atr)
            if self.game.pieces[u].atr['pos'][2]-1 >= 0:
                self.game.pieces[u].atr['rel'] = self.board[self.game.pieces[u].atr['pos'][1]-1][self.game.pieces[u].atr['pos'][2]-1][self.game.pieces[u].atr['pos'][0]-1]
                self.board[self.game.pieces[u].atr['pos'][1]-1][self.game.pieces[u].atr['pos'][2]-1][self.game.pieces[u].atr['pos'][0]-1].atr['rel'] = self.game.pieces[u]
            if self.game.pieces[u].atr['moved_last_turn'] == True:
                self.rendersi(self.game.pieces[u].atr,'piece')
        if not None in self.game.moved_from_last_turn:
            self.board[self.game.moved_from_last_turn[1]-1][self.game.moved_from_last_turn[2]-1][self.game.moved_from_last_turn[0]-1].atr['obj'].setTexture(self.colour[3][2][1])
        self.step = True

    def unrenders(self):
        self.step = False
        for u in range(0,len(self.game.pieces)):
            self.game.pieces[u].atr['obj'].removeNode()
            time.sleep(0.01)
        self.step = True

    def rendersboard(self):
        self.step = False
        self.board = []
        for boardx in range(0,8):
            self.board.append([])
            for boardy in range(0,8):
                self.board[boardx].append([])
                for boardz in range(0,8):
                    self.board[boardx][boardy].append(boardc([boardz+1,boardx+1,boardy+1],self.colour[2][boardx%2][boardy%2][boardz%2]))
                    self.board[boardx][boardy][boardz].atr['obj'] = loader.loadModel(f'board2.dae')
                    self.board[boardx][boardy][boardz].atr['obj'].reparentTo(render)
                    self.board[boardx][boardy][boardz].atr['obj'].setPos(boardx*self.game_size+self.game_size,boardy*self.game_size+0.01+0.5*self.game_size,boardz*self.game_size+self.game_size)
                    self.board[boardx][boardy][boardz].atr['obj'].setScale(self.half_game_size,self.half_game_size,self.half_game_size)
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
        piece.atr['obj'] = loader.loadModel(f'{piece.atr["typ"]}.dae')
        piece.atr['obj'].reparentTo(render)
        piece.atr['obj'].setPos(piece.atr['pos'][1]*self.game_size,piece.atr['pos'][2]*self.game_size,piece.atr['pos'][0]*self.game_size)
        piece.atr['obj'].setScale(self.half_game_size,self.half_game_size,self.half_game_size)
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
        loader.unloadModel(f'{piece.atr["typ"]}.dae')
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
            elif not None in self.game.moved_from_last_turn:
                if highlightpiece == self.board[self.game.moved_from_last_turn[1]-1][self.game.moved_from_last_turn[2]-1][self.game.moved_from_last_turn[0]-1].atr:
                    color = self.colour[3][2][1]
                else:
                    color = highlightpiece['col']
            else:
                color = highlightpiece['col']
        highlightpiece['obj'].setTexture(color)

    def click(self):
        #Change to move(x,y,z)
        self.move.ox = 0
        self.move.oy = 0
        self.move.oz = 0
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
                self.move.ox = self.pickedObjp['pos'][0]
                self.move.oy = self.pickedObjp['pos'][1]
                self.move.oz = self.pickedObjp['pos'][2]

    def click2(self):
        self.move.nx = 0
        self.move.ny = 0
        self.move.nz = 0
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
                    self.move.nx = self.pickedObjb['pos'][0]
                    self.move.ny = self.pickedObjb['pos'][1]
                    self.move.nz = self.pickedObjb['pos'][2]
                else:
                    self.move.nx = self.pickedObjc['pos'][0]
                    self.move.ny = self.pickedObjc['pos'][1]
                    self.move.nz = self.pickedObjc['pos'][2]

    def stuff2(self):
        self.reset2()
        if self.game.gameover == 1 or self.game.gameover == 2:
            print('The game is already over!\n')
            time.sleep(0.1)
            return
        self.valid = 1
        if self.move.ox == 0 or self.move.oy == 0 or self.move.oz == 0:
            print('You must select a piece to move\n')
            self.valid = 0
        elif self.move.oz < 0:
            print('You may not move a piece that has already been captured\n')
            self.valid = 0
        if self.move.nx == 0 or self.move.ny == 0 or self.move.nz == 0:
            print('You must select a place to move to\n')
            self.valid = 0
        elif self.move.nz < 0:
            print('You may not capture a piece that has already been captured\n')
            self.valid = 0
        if self.valid == 1:
            self.move.findpiece()
        self.move.nx = 0
        self.move.ny = 0
        self.move.nz = 0
        if hasattr(self.move,'valid'):
            if self.move.valid == 1:
                self.reset()
                self.move.ox = 0
                self.move.oy = 0
                self.move.oz = 0

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

    def init(self):
        
        self.nout = MultiplexStream()
        Notify.ptr().setOstreamPtr(self.nout, 0)
        self.nout.addFile(Filename("panda3doutput.txt"))

        #ShowBase.__init__(self)
        base = ShowBase()

        render.setShaderAuto()
        base.disableMouse()
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
            self.boards.append(loader.loadModel(f'board.dae'))
            self.boards[u].reparentTo(render)
            self.boards[u].setPos(self.multiplied_game_size,(u+0.5)*self.game_size,self.multiplied_game_size)
            self.boards[u].setScale(self.half_game_size,self.half_game_size,self.half_game_size)
            self.boards[u].setHpr(0,0,90)
            self.boards[u].setTexture(self.colour[1][0][u%2])

        for u in range(0,4):
            self.posts.append(loader.loadModel(f'post.dae'))
            self.posts[u].reparentTo(render)
            self.posts[u].setPos(self.multiplied_game_size+self.post[u][0]*self.game_size,self.game_size*4,self.multiplied_game_size+self.post[u][1]*self.game_size)
            self.posts[u].setScale(self.half_game_size,self.half_game_size,self.half_game_size)
            self.posts[u].setTexture(self.colour[1][1])

        self.renders()

class key_control():
    def __init__(self, key, function):

        self.key = key
        self.function = function

        self.pressed = 0
        base.accept(key, self.setKey, [1])

    def setKey(self, value):
        self.pressed = value

class movement_control(key_control):
    def __init__(self, key, function, movement_type):

        super().__init__(key, function)
        self.movement_type = movement_type
        base.accept(f'{key}-up', self.setKey, [0])

    def key_press(self, distance):
        self.function(distance)

class hotkey_control(key_control):
    def __init__(self, key, function):

        super().__init__(key, function)

    def key_press(self):
        self.function()
        self.setKey(0)

class boardc:
    def __init__(self,pos,col):
        self.atr = {'pos':pos,'col':col,'moved_last_turn':False,'ispicked1':False,'ispicked2':False}
