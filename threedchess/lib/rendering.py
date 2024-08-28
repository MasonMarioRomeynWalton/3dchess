from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

import threading
import time
import itertools

from . import controlable_camera

home = "../../3dchess"

class rendering_task(threading.Thread):
    def __init__(self, move, game):
        threading.Thread.__init__(self)


        ## The game object
        self.game = game

        #To merge
        self.move = move

        ## initialize the panda3d environment window
        self.initialize_panda3d_environment()

        ## Render all of the 3d models
        self.render_all_3d_models()



        ## The maximum distance the camera can be from the board
        max_distance_away = max(
            self.game.size_of_dimensions[0],
            self.game.size_of_dimensions[1],
            self.game.size_of_dimensions[2]
        )

        ## Create the camera 
        self.camera = controlable_camera(max_distance_away,1,0.15)
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
            hotkey_control(  'f',      self.camera.init_center),
            hotkey_control(  'mouse1', self.select_move_piece),
            hotkey_control(  'mouse3', self.select_capture_location),
            hotkey_control(  'enter',  self.stuff2)
        ]

        self.step = True

    def initialize_panda3d_environment(self):
        ## Create the error stream
        ## Unable to find documentation
        self.nout = MultiplexStream()
        Notify.ptr().setOstreamPtr(self.nout, 0)
        self.nout.addFile(Filename("panda3doutput.txt"))

        ## Create panda3d environment
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

    def render_all_3d_models(self):
        
        colour_list = []
        for i in range(0,8):
            colour_list.append(f'board_{i}')

        for i in range(0,2):
            colour_list.append(f'player_{i}')
            colour_list.append(f'move_piece_{i}')
            colour_list.append(f'capture_piece_{i}')
            colour_list.append(f'last_moved_piece_{i}')

        colour_list.append('grid')
        colour_list.append('post')

        self.colour_map = {}
        for colour in colour_list:
            self.colour_map[colour] = loader.loadTexture(f'{home}/static/maps/{colour}.png')
            self.colour_map[f'{colour}'].setMagfilter(SamplerState.FT_nearest)


        self.directionalLight = [[45,0,0],[135,0,0],[45,180,0],[135,180,0],[45,30,0],[45,-30,0],[135,30,0],[135,-30,0],[45,150,0],[45,-150,0],[135,150,0],[135,-150,0]]
        self.directionalLights = []
        self.directionalLightNP= []
        for u in range(0,12):
            self.directionalLights.append(DirectionalLight('directionalLight'))
            self.directionalLights[u].setColor((0.3, 0.3, 0.3, 1))
            self.directionalLightNP.append(render.attachNewNode(self.directionalLights[u]))
            self.directionalLightNP[u].setHpr(self.directionalLight[u][0],self.directionalLight[u][1],self.directionalLight[u][2])
            render.setLight(self.directionalLightNP[u])

        self.render_posts()

        self.boards = []

        self.board = []
        self.renders_board(self.board, [0,0,0], self.game.dimensions)

        #self.renders()

    def render_generic_object(self, model, texture, game_position = [0,0,0], rotation = [0,0,0], scale = [1,1,1]):
        rendered_object = loader.loadModel(model)
        rendered_object.reparentTo(render)

        rendering_position = []
        for i in range(0,self.game.dimensions):
            rendering_position.append(game_position[i]-(self.game.size_of_dimensions[i]-1)/2)

        rendered_object.setPos(
            rendering_position[0],
            rendering_position[2],
            rendering_position[1]
        )

        rendered_object.setScale(
            scale[0]/2,
            scale[2]/2,
            scale[1]/2
        )

        rendered_object.setHpr(
            rotation[0],
            rotation[1],
            rotation[2]
        )

        if texture != None:
            rendered_object.setTexture(self.colour_map[texture])

        return rendered_object


    def render_posts(self):
        
        ## Create the 3 dimensional grid of posts
        post_grid = [
            [-0.5,self.game.size_of_dimensions[0]-0.5],
            [-0.5,self.game.size_of_dimensions[1]-0.5],
            [self.game.size_of_dimensions[2]/2-0.5]
        ]

        
        ## Generate the cartesian product of post locations
        post_locations = itertools.product(*post_grid)

        ## Generate the posts
        self.posts = []
        for post_location in post_locations:
            self.posts.append(self.render_generic_object(
                'post.dae',
                'post',
                post_location,
                scale = [1,1,self.game.size_of_dimensions[2]-0.5]
            ))


    def renders_board(self, board, pos, dimensions):
        ## renders the board
        if dimensions == 0:
            top_colour = self.calculate_top_colour(pos)
            bottom_colour = self.calculate_bottom_colour(pos)

            board_segment = board_segment_render(
                pos,
                self.colour_map[f'board_{top_colour}']
            )

            
                    
            board_segment.obj = self.render_generic_object(
                'board_piece.dae',
                f'board_{top_colour}',
                pos
            )

            ## The bottom section of the board is rendered slightly lower than the top
            pos[2] = pos[2] - 0.001


            board_segment.bottom = self.render_generic_object(
                'board_piece.dae',
                None,
                pos
            )

            board_segment.bottom.setColorScale(bottom_colour[0],bottom_colour[1],bottom_colour[2],0)

        else:
            for sub_board in range(0,self.game.size_of_dimensions[dimensions-1]):
                board.append([])
                sub_board_pos = pos.copy()
                sub_board_pos[dimensions-1] = sub_board
                self.renders_board(board[-1], sub_board_pos, dimensions-1)

    def calculate_top_colour(self, pos):
        ## This is not possible in higher dimensions
        ## Cardinals can move to all squares on the board in 4d chess

        if self.game.dimensions == 1:
            colour_index = 0

        elif self.game.dimensions == 3:
            colour_index = (pos[0]%2+(pos[1]%2)*2+(pos[2]%2)*4)%8

        else:
            colour_index = sum(pos)%2
            if colour_index == 1:
                colour_index = 7

        return colour_index

    def calculate_bottom_colour(self, pos):
        colour = [0,0,0]
        for i in range(0,self.game.dimensions):
            colour[i] = pos[i]/self.game.size_of_dimensions[i]

        return colour

    def unrenders_board(self):
        self.step = False
        for boardx in range(0,8):
            for boardy in range(0,8):
                for boardz in range(0,8):
                    self.board[boardx][boardy][boardz].atr['obj'].removeNode()
                    time.sleep(0.01)
        self.step = True

    def renders(self):
        ## renders all the pieces
        self.step = False
        for u in range (0,len(self.game.pieces)):
            self.game.pieces[u].atr['obj'] = loader.loadModel(f'{self.game.pieces[u].atr["typ"]}.dae')
            self.game.pieces[u].atr['obj'].reparentTo(render)
            self.game.pieces[u].atr['obj'].setPos(self.game.pieces[u].atr['pos'][1]*self.game_size,self.game.pieces[u].atr['pos'][2]*self.game_size,self.game.pieces[u].atr['pos'][0]*self.game_size)
            self.game.pieces[u].atr['obj'].setScale(self.half_game_size,self.half_game_size,self.half_game_size)
            if self.game.pieces[u].atr['col'] == 0:
                self.game.pieces[u].atr['obj'].setTexture(self.colour_map[f'player_0'], 1)
                self.game.pieces[u].atr['obj'].setHpr(0,0,180)
            if self.game.pieces[u].atr['col'] == 1:
                self.game.pieces[u].atr['obj'].setTexture(self.colour_map[f'player_1'], 1)
                self.game.pieces[u].atr['obj'].setHpr(0,0,0)

            self.game.pieces[u].atr['obj'].setPythonTag('piece',self.game.pieces[u].atr)
            if self.game.pieces[u].atr['pos'][2]-1 >= 0:
                self.game.pieces[u].atr['rel'] = self.board[self.game.pieces[u].atr['pos'][1]-1][self.game.pieces[u].atr['pos'][2]-1][self.game.pieces[u].atr['pos'][0]-1]
                self.board[self.game.pieces[u].atr['pos'][1]-1][self.game.pieces[u].atr['pos'][2]-1][self.game.pieces[u].atr['pos'][0]-1].atr['rel'] = self.game.pieces[u]
            if self.game.pieces[u].atr['moved_last_turn'] == True:
                self.rendersi(self.game.pieces[u].atr,'piece')
        if not None in self.game.moved_from_last_turn:
            self.board[self.game.moved_from_last_turn[1]-1][self.game.moved_from_last_turn[2]-1][self.game.moved_from_last_turn[0]-1].atr['obj'].setTexture(self.colour_map['last_moved_board'])
        self.step = True

    def reset():
        self.unrenders()
        self.unrenders_board()
        self.renders_board(self.board, [0,0,0], self.game.dimensions)
        self.renders()

    def unrenders(self):
        ## unrenders all the pieces
        self.step = False
        for u in range(0,len(self.game.pieces)):
            self.game.pieces[u].atr['obj'].removeNode()
            time.sleep(0.01)
        self.step = True
    def rerenders(self,piece):
        self.step = False
        piece.atr['obj'] = loader.loadModel(f'{piece.atr["typ"]}.dae')
        piece.atr['obj'].reparentTo(render)
        piece.atr['obj'].setPos(piece.atr['pos'][1]*self.game_size,piece.atr['pos'][2]*self.game_size,piece.atr['pos'][0]*self.game_size)
        piece.atr['obj'].setScale(self.half_game_size,self.half_game_size,self.half_game_size)
        if piece.atr['col'] == 0:
            piece.atr['obj'].setTexture(self.colourmap['piece_0'], 1)
            piece.atr['obj'].setHpr(0,0,180)
        if piece.atr['col'] == 1:
            piece.atr['obj'].setTexture(self.colourmap['piece_1'], 1)
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
                if highlightpiece['col'] == 0:
                    color = self.colour_map['capture_piece_0']
                if highlightpiece['col'] == 1:
                    color = self.colour_map['capture_piece_1']
            if piecetype == 'board':
                color = self.colour_map['capture_board']
        if highlightpiece['moved_last_turn'] == True:
            if highlightpiece['col'] == 0:
                color = self.colour_map['last_moved_piece_0']
            if highlightpiece['col'] == 1:
                color = self.colour_map['last_moved_piece_1']
        if highlightpiece['ispicked1'] == True:
            if highlightpiece['col'] == 0:
                color = self.colour_map['move_piece_0']
            if highlightpiece['col'] == 1:
                color = self.colour_map['move_piece_1']
        if highlightpiece['ispicked1'] == False and highlightpiece['ispicked2'] == False and highlightpiece['moved_last_turn'] == False:
            if highlightpiece['col'] == 0:
                color = self.colour_map['player_0']
            elif highlightpiece['col'] == 1:
                color = self.colour_map['player_1']
            elif not None in self.game.moved_from_last_turn:
                if highlightpiece == self.board[self.game.moved_from_last_turn[1]-1][self.game.moved_from_last_turn[2]-1][self.game.moved_from_last_turn[0]-1].atr:
                    color = self.colour_map['last_moved_board']
                else:
                    color = highlightpiece.col
            else:
                color = highlightpiece.col
        highlightpiece['obj'].setTexture(color)

    def select_move_piece(self):
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

    def select_capture_location(self):
        print('select_capture_location')
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
            print('picked something')
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

    def reset_piece_colour(self):
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

class board_segment_render():
    def __init__(self,pos,col):
        self.pos = pos
        self.col = col
        self.moved_last_turn = False
        self.ispicked1 = False
        self.ispicked2 = False


class piece_render():
    def __init__():
        self.is_picked1 = False
        self.is_picked2 = False



