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

        ## The direction the player's pieces are facing
        self.player_rotation = {'0':180,'1':0}

        ## The piece that is picked for moving
        self.picked_for_move = None

        ## The board segment that is picked for being moved to
        self.picked_for_capture_board = None

        ## The piece that is picked for capture
        self.picked_for_capture = None

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
        self.camera = controlable_camera(max_distance_away,0.5,0.1)
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
        
        # Get these from file

        colour_list = []
        for i in range(0,8):
            colour_list.append(f'board_{i}')

        for i in range(0,2):
            colour_list.append(f'player_{i}')
            colour_list.append(f'move_piece_{i}')
            colour_list.append(f'capture_piece_{i}')
            colour_list.append(f'last_moved_piece_{i}')

        colour_list.append(f'capture_board')

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

        self.board = []
        self.render_board(self.board, [0,0,0], self.game.dimensions)

        self.board[3][2][1][0].obj.setTexture(self.colour_map['post'])

        self.render_pieces()

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
            [self.game.size_of_dimensions[2]/2-1]
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


    def render_board(self, board, pos, dimensions):
        ## renders the board
        if dimensions == 0:
            top_colour = self.calculate_top_colour(pos)
            bottom_colour = self.calculate_bottom_colour(pos)

            current_board_segment_render = board_segment_render(
                pos,
                self.colour_map[f'board_{top_colour}']
            )

            board.append(current_board_segment_render)
                    
            ## Because the board is rendered slightly lower than the pieces
            pos[2] = pos[2] - 0.5

            current_board_segment_render.obj = self.render_generic_object(
                'board_piece.dae',
                f'board_{top_colour}',
                pos

            )

            current_board_segment_render.obj.setPythonTag('object_attributes', current_board_segment_render)

            ## The bottom section of the board is rendered slightly lower than the top
            pos[2] = pos[2] - 0.00005


            current_board_segment_render.bottom = self.render_generic_object(
                'board_piece.dae',
                None,
                pos
            )

            current_board_segment_render.bottom.setColorScale(bottom_colour[0],bottom_colour[1],bottom_colour[2],0)

        else:
            for sub_board in range(0,self.game.size_of_dimensions[dimensions-1]):
                board.append([])
                sub_board_pos = pos.copy()
                sub_board_pos[dimensions-1] = sub_board
                self.render_board(board[-1], sub_board_pos, dimensions-1)

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

        percent_along_board = []
        for i in range(0,3):
            percent_along_board.append(pos[i]/(self.game.size_of_dimensions[i]-1))

        percent_along_board[0] = percent_along_board[0]
        percent_along_board[2] = 1-percent_along_board[2]

        colour = [
            1-percent_along_board[0]/2-percent_along_board[1]/2,
            1-percent_along_board[0]/2-percent_along_board[1]/2-percent_along_board[2]/2,
            1-percent_along_board[0]/2-percent_along_board[2]/2
        ]

        return colour

    def unrender_board(self):
        self.step = False
        for boardx in range(0,8):
            for boardy in range(0,8):
                for boardz in range(0,8):
                    self.board[boardx][boardy][boardz].atr['obj'].removeNode()
                    time.sleep(0.01)
        self.step = True

    def render_pieces(self):
        ## renders all the pieces
        


        for piece in self.game.pieces:

            current_piece_render = piece_render(piece.atr['pos'], piece.atr['col'])

            current_piece_render.obj = self.render_generic_object(
                f'{piece.atr["typ"]}.dae',
                f'player_{piece.atr["col"]}',
                piece.atr['pos'],
                [0,0,self.player_rotation[str(piece.atr["col"])]],
            )

            current_piece_render.obj.setPythonTag('object_attributes', current_piece_render)

            self.board[piece.atr['pos'][2]][piece.atr['pos'][1]][piece.atr['pos'][0]][0].rel = current_piece_render



            #self.game.pieces[u].atr['obj'].setPythonTag('piece',self.game.pieces[u].atr)
            #if self.game.pieces[u].atr['pos'][2]-1 >= 0:
            #    self.game.pieces[u].atr['rel'] = self.board[self.game.pieces[u].atr['pos'][1]-1][self.game.pieces[u].atr['pos'][2]-1][self.game.pieces[u].atr['pos'][0]-1]
            #    self.board[self.game.pieces[u].atr['pos'][1]-1][self.game.pieces[u].atr['pos'][2]-1][self.game.pieces[u].atr['pos'][0]-1].atr['rel'] = self.game.pieces[u]
            #if self.game.pieces[u].atr['moved_last_turn'] == True:
            #    self.highlight_piece(self.game.pieces[u].atr,'piece')

        if not None in self.game.moved_from_last_turn:
            self.board[self.game.moved_from_last_turn[1]-1][self.game.moved_from_last_turn[2]-1][self.game.moved_from_last_turn[0]-1].atr['obj'].setTexture(self.colour_map['last_moved_board'])

    def reset():
        self.unrenders()
        self.unrender_board()
        self.render_board(self.board, [0,0,0], self.game.dimensions)
        self.renders()

    def unrenders(self):
        ## unrenders all the pieces
        self.step = False
        for u in range(0,len(self.game.pieces)):
            self.game.pieces[u].atr['obj'].removeNode()
            time.sleep(0.01)
        self.step = True

    def create_piece(self,piece):
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
        self.highlight_piece(piece.atr,'piece')

    def remove_piece(self,piece):
        self.step = False
        piece.atr['obj'].removeNode()
        time.sleep(0.01)
        loader.unloadModel(f'{piece.atr["typ"]}.dae')
        self.step = True

    def highlight_piece(self,highlight_piece,piecetype):
        ## Modify the colour of a piece to the piece status with the highest priority

        ## If the piece is picked to be moved
        if highlight_piece.is_picked_for_move == True:
            colour = self.colour_map[f'move_piece_{highlight_piece.colour}']

        ## If the piece is picked to be captured
        elif highlight_piece.is_picked_for_capture == True:
            if piecetype == 'piece':
                colour = self.colour_map[f'capture_piece_{highlight_piece.colour}']
            elif piecetype == 'board':
                colour = self.colour_map[f'capture_board']

        ## If the piece has been moved or moved from in the last turn
        elif highlight_piece.moved_last_turn == True:
            if piecetype == 'piece':
                colour = self.colour_map[f'last_moved_piece_{highlight_piece.colour}']
            elif piecetype == 'board':
                colour = self.colour_map[f'last_moved_board']

        ## Unhighlight the piece
        else:
            if piecetype == 'piece':
                colour = self.colour_map[f'player_{highlight_piece.colour}']
            elif piecetype == 'board':
                if highlight_piece.position == self.game.moved_from_last_turn:
                    colour = self.colour_map['last_moved_board']
                else:
                    colour = highlight_piece.colour

        highlight_piece.obj.setTexture(colour)


    def select_move_piece(self):
        #Change to move(x,y,z)

        if self.picked_for_move != None:
            self.picked_for_move.is_picked_for_move = False
            self.highlight_piece(self.picked_for_move,'piece')
            self.picked_for_move = None

        self.move.ox = 0
        self.move.oy = 0
        self.move.oz = 0

        try:
            mpos = base.mouseWatcherNode.getMouse()
        except:
            print('You clicked off the screen\n')

        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        self.myTraverser.traverse(render)
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            pickedObj = self.queue.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetPythonTag('object_attributes')
            pickedObj = pickedObj.getNetPythonTag('object_attributes')

            if type(pickedObj) == piece_render:
                self.picked_for_move = pickedObj
                self.picked_for_move.is_picked_for_move = True
                self.highlight_piece(self.picked_for_move,'piece')
                self.move.ox = self.picked_for_move.position[0]
                self.move.oy = self.picked_for_move.position[1]
                self.move.oz = self.picked_for_move.position[2]

    def select_capture_location(self):

        self.move.nx = 0
        self.move.ny = 0
        self.move.nz = 0
        self.reset2()

        if self.picked_for_capture != None:
            self.picked_for_capture.is_picked_for_capture = False
            self.highlight_piece(self.picked_for_capture,'piece')
            self.picked_for_capture = None

        if self.picked_for_capture_board != None:
            self.picked_for_capture_board.is_picked_for_capture = False
            self.highlight_piece(self.picked_for_capture_board,'board')
            self.picked_for_capture = None

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
            pickedObj = pickedObj.findNetPythonTag('object_attributes')
            pickedObj = pickedObj.getNetPythonTag('object_attributes')

            if type(pickedObj) == board_segment_render:
                self.picked_for_capture_board = pickedObj
                if self.picked_for_capture_board.rel != None:
                    self.picked_for_capture = self.picked_for_capture_board.rel
                else:
                    self.picked_for_capture = None
            
            if type(pickedObj) == piece_render:
                self.picked_for_capture = pickedObj
                self.picked_for_capture_board = self.board[self.picked_for_capture.position[2]][self.picked_for_capture.position[1]][self.picked_for_capture.position[0]][0]

            if self.picked_for_capture_board != None:
                self.picked_for_capture_board.is_picked_for_capture = True
                self.highlight_piece(self.picked_for_capture_board, 'board')

            if self.picked_for_capture != None:
                self.picked_for_capture.is_picked_for_capture = True
                self.highlight_piece(self.picked_for_capture, 'piece')


            # Add ox ny stuff

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

    ## Unused?
    def reset_piece_colour(self):
        if hasattr(self,'pickedObjp'):
            if self.pickedObjp != None:
                self.pickedObjp['ispicked1'] = False
                self.highlight_piece(self.pickedObjp,'piece')

    def reset2(self):
        if hasattr(self,'pickedObjc'):
            if self.pickedObjc != None:
                self.pickedObjc['ispicked2'] = False
                self.highlight_piece(self.pickedObjc,'piece')
                del self.pickedObjc
        if hasattr(self,'pickedObjb'):
            if self.pickedObjb != None:
                self.pickedObjb['ispicked2'] = False
                self.highlight_piece(self.pickedObjb,'piece')
                del self.pickedObjb


    # Merge these two
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
    def __init__(self, position, colour):
        
        ## Need for knowing the position of where to move to
        self.position = position

        self.rel = None

        self.colour = colour
        self.is_picked_for_move = None
        self.picked_for_capture = False
        self.moved_last_turn = False

class piece_render():
    def __init__(self, position, colour):


        ## Needed for knowing the position of where to move from
        self.position = position

        ## Needed for knowing which colour to render the pieces
        self.colour = colour

        self.is_picked_for_move = False
        self.is_picked_for_capture = False
        self.moved_last_turn = False



