import os

import numpy
import json

from . import move
from . import rendering_task
from . import piece_layouts

home = "../3dchess"

class game():
    def __init__(self, across_dimensions = 2, side_dimensions = 1, size_of_dimensions = (8,8,8)):

        self.across_dimensions = across_dimensions
        self.side_dimensions = side_dimensions
        self.dimensions = self.across_dimensions + self.side_dimensions
        self.unused_dimensions = 3 - self.dimensions
        self.size_of_dimensions = size_of_dimensions

        self.renders = [rendering_task(self)]

    def restart(self):
        ##For starting a game of the same type

        self.turn = 0

        ## Determines where the next capture piece should go
        self.next_captured_pos_white = (9,9,9)
        self.next_captured_pos_black = (
            (-2,)*self.across_dimensions +
            (0,)*self.side_dimensions
        )

        ## Initialises global variables
        self.moved_from_last_turn = (None,None,None)
        self.enpass = (None,None,None)
        self.gameover = False

        ## Create the board
        self.board = numpy.empty(self.size_of_dimensions, dtype=object)

        ## Import the layour of the pieces
        self.layout = piece_layouts.get_piece_layout(
            self.dimensions,
            self.size_of_dimensions,
            self.unused_dimensions,
            self.across_dimensions,
            self.side_dimensions
        )


        ## Load all the pieces
        white_pieces = [
            game_piece(
                piece['piece_type'],
                piece['position'],
                0
            )
            for piece in self.layout
        ]

        ## Finds where the black pieces by mirroring the white pieces
        black_pieces = [
            game_piece(
                piece['piece_type'],
                tuple(
                    self.size_of_dimensions[0:self.across_dimensions][i] -
                    piece['position'][0:self.across_dimensions][i] -
                    1
                    for i in range(self.across_dimensions)
                ) + (piece['position'][self.across_dimensions:]),
                1
            )
            for piece in self.layout
        ]

        self.pieces = white_pieces + black_pieces



        ## Add the pieces to the board
        for piece in self.pieces:
           self.board[piece.position] = piece 

        ## Initialise the savefile
        self.update_save()



    def create_piece(self, piece_type, position, colour, has_moved = False, moved_last_turn = False):
        self.pieces.append(game_piece(piece_type, position, colour, has_moved, moved_last_turn))

    ## Attempt to move a piece
    def attempt_move(self, render, old_position, new_position):
        my_move = move(self, render, old_position, new_position)

        if my_move.is_valid == True:
            self.move_piece(old_position, new_position, 'main')
            self.update_turn()

        return my_move.is_valid

    ## Actually move a piece
    def move_piece(self, old_position, new_position, move_type):

        piece = self.board[old_position]

        for render in self.renders:
            if move_type == 'main':
                render.unhighlight_last_moved_piece()
                render.unhighlight_last_moved_board()
            render.unrender_piece(piece)

        piece.position = new_position
        piece.moved_last_turn = True
        piece.has_moved = True

        # Something about the render?
        if all([(new_position[i] < self.size_of_dimensions[i] and
                 new_position[i] >= 0
                )
                for i in range(self.dimensions)]):
            self.board[old_position] = None
            self.board[new_position] = piece

        ## For each rendering of the board
        for render in self.renders:
            render.render_piece(piece)
            if move_type == 'main':
                render.highlight_last_moved_board(old_position)
                render.highlight_last_moved_piece(new_position)

        if move_type == 'capture':
            print(f'A {piece.colour} {piece.piece_type} has been captured!\n')

        # Todo
        #if piece.piece_type == 'king':
        #    self.gameover = True
        #    print (f'player {1-piece.colour} wins!\n')

        self.update_save()

    def update_turn(self):
        if self.turn == 0:
            self.turn = 1
            print('Black\'s turn\n')
        elif self.turn == 1:
            self.turn = 0
            print('White\'s turn\n')

    ## Creates a new save
    def update_save(self):

        misc_save = {'turn':self.turn,
                     'next_captured_pos_white':self.next_captured_pos_white,
                     'next_captured_pos_black':self.next_captured_pos_black,
                     'moved_from_last_turn':self.moved_from_last_turn,
                     'enpass':self.enpass,
                     'gameover':self.gameover
                    }

        ## Convert to json
        json_save = json.dumps(misc_save, indent=4)
        ## Write to file
        with open(f'{home}/public/misc.txt', 'w+') as f:
            f.writelines(json_save)

        piece_save = []
        for piece in self.pieces:
            piece_save.append({'piece_type':piece.piece_type,
                              'colour':piece.colour,
                              'position':piece.position,
                              'has_moved':piece.has_moved,
                              'moved_last_turn':piece.moved_last_turn
                             })

        ## Convert to json
        json_save = json.dumps(piece_save, indent=4)
        ## Write to file
        with open(f'{home}/public/pieces.txt', 'w+') as f:
            f.writelines(json_save)

    def open_from_save(self):

        with open(f'{home}/public/misc.txt','r') as f:
            json_misc_save = f.read()
        misc_save = json.loads(json_misc_save)


        self.turn = misc_save['turn']
        self.next_captured_pos_white = misc_save['next_captured_pos_white']
        self.next_captured_pos_black = misc_save['next_captured_pos_black']
        self.moved_from_last_turn = misc_save['moved_from_last_turn']
        self.enpass = misc_save['enpass']
        self.gameover = misc_save['gameover']

        self.board = numpy.empty(self.size_of_dimensions, dtype=object)

        with open(f'{home}/public/pieces.txt','r') as f:
            json_piece_save = f.read()
        piece_save = json.loads(json_piece_save)

        self.pieces = [
            game_piece(piece['piece_type'],
                              piece['position'],
                              piece['colour'],
                              piece['has_moved'],
                              piece['moved_last_turn']
                             )
            for piece in piece_save
        ]

    def write(self,file,prefix,content,piece_num):
        return

class game_board:
    def __init__(self):
        pass

class game_piece:
    def __init__(self,piece_type, position, colour, has_moved = False, moved_last_turn = False):
        self.piece_type = piece_type
        self.position = position
        self.colour = colour
        self.has_moved = has_moved
        self.moved_last_turn = moved_last_turn
        self.rendering = None
