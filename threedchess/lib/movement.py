# Maybe make different movement types different classes
class move:
    def __init__(self, game, render, old_position, new_position, castling_movement = False):

        self.game = game
        self.render = render

        ## The old position of the piece
        self.old_position = old_position

        ## The new position of the piece
        self.new_position = new_position

        self.distance_between_positions = tuple(
            abs(self.old_position[i] - self.new_position[i])
            for i in range(self.game.dimensions)
        )

        self.sorted_distance = tuple(sorted(
            (distance for distance in self.distance_between_positions
             if distance != 0
            )
        ))

        # Not sure
        self.castling_movement = castling_movement

        ## Checks if the move is valid
        self.is_valid = self.process_move()


    ## Process a move attempt
    ## Returns whether or not the move was valid
    def process_move(self):
        ## Check if the game is over
        if self.game.gameover == 1 or self.game.gameover == 2:
            print('The game is already over!\n')
            return False

        ## If two locations are the same
        if all(distance == 0 for distance in self.distance_between_positions):
            print('The two specified locations must be different\n')
            return False

        ## Find the piece being moved
        self.piece = self.game.board[(self.old_position)]
        if self.piece == None:
            print('This is not a valid piece\n')
            return False

        ## Check if the piece is a valid colour
        if not self.piece.colour == self.game.turn:
            print('This piece is not a valid colour\n')
            return False

        ## Find if there's a piece in the new location
        self.piece_for_capture = self.game.board[(self.new_position)]

        ## Check if there is already have a piece in the new location
        if (self.piece_for_capture != None):
            if self.piece.colour == self.piece_for_capture.colour:
                print('You already have a piece here\n')
                return False
            else:
                self.capture = True
        else:
            self.capture = False


#        if self.piece.atr['typ'] == 'king':
#            if self.dx == 2 and self.dy == 0 and self.dz == 0:
#                if(self.rookpath())
#                    self.castlingvar = True
#                    self.castling()
#                    self.castlingvar = False
#            elif (self.dx > 1 or self.dy > 1 and self.dz > 1):
#                print('This is not a valid location\n')
#                return 0
#
#        if self.piece.atr['typ'] == 'pawn':
#            if self.capture == 1:
#                if (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 1:
#                    print('Pawns can only capture on sideways diagonals\n')
#                    self.valid = 0
#                elif (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dx == 1 and self.dl[0] == 0 and self.dl[1] == 1 and self.dl[2] == 1:
#                    pass
#                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 1 and self.dl[1] == 1 and self.dl[2] == 1:
#                    pass
#                else:
#                    print('This is not a valid location\n')
#                    self.valid = 0
#            if self.capture == 0:
#                if (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 1:
#                    pass
#                elif (self.ny - self.oy == game.turn*2 or self.nz - self.oz == game.turn*2) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 2:
#                    if self.piece.atr['first'] == 0:
#                        self.rookpath()
#                        self.enpass2 = [int((self.ox+self.nx)/2), int((self.oy+self.ny)/2), int((self.oz+self.nz)/2)]
#                    else:
#                        print('Pawns can only double step on their first turn\n')
#                        self.valid = 0
#                elif (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dx == 1 and self.dl[0] == 0 and self.dl[1] == 1 and self.dl[2] == 1:
#                    if game.enpass[0] == self.nx and game.enpass[1] == self.ny and game.enpass[2] == self.nz:
#                        for piecetwo in range(len(game.pieces)):
#                            if game.pieces[piecetwo].atr['moved_last_turn'] == True:
#                                self.capture = 1
#                                break
#                    else:
#                        print('Pawns can only move on sideways diagonals to capture\n')
#                        self.valid = 0
#                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 1 and self.dl[1] == 1 and self.dl[2] == 1:
#                    if game.enpass[0] == self.nx and game.enpass[1] == self.ny and game.enpass[2] == self.nz:
#                        for piecetwo in range(len(game.pieces)):
#                            if game.pieces[piecetwo].atr['moved_last_turn'] == True:
#                                self.capture = 1
#                                break
#                    else:
#                        print('Pawns can only move on sideways diagonals to capture\n')
#                        self.valid = 0
#                else:
#                    print('This is not a valid location\n')
#                    self.valid = 0
#        if self.piece.atr['typ'] == 'peasant':
#            if self.capture == 1:
#                if (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 1:
#                    print('Peasants can only capture on three dimensional diagonals\n')
#                    self.valid = 0
#                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 1 and self.dl[2] == 1:
#                    print('Peasants can only capture on three dimensional diagonals\n')
#                    self.valid = 0
#                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 1 and self.dl[1] == 1 and self.dl[2] == 1:
#                    pass
#                else:
#                    print('This is not a valid location\n')
#                    self.valid = 0
#            if self.capture == 0:
#                if (self.ny - self.oy == game.turn or self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 1:
#                    pass
#                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 0 and self.dl[1] == 1 and self.dl[2] == 1:
#                    pass
#                elif (self.ny - self.oy == game.turn*2 or self.nz - self.oz == game.turn*2) and self.dl[0] == 0 and self.dl[1] == 0 and self.dl[2] == 2:
#                    if self.piece.atr['first'] == 0:
#                        self.rookpath()
#                        self.enpass2 = [int((self.ox+self.nx)/2), int((self.oy+self.ny)/2), int((self.oz+self.nz)/2)]
#                    else:
#                        print('Peasants can only double step on their first turn\n')
#                        self.valid = 0
#                elif (self.ny - self.oy == game.turn*2 and self.nz - self.oz == game.turn*2) and self.dl[0] == 0 and self.dl[1] == 2 and self.dl[2] == 2:
#                    if self.piece.atr['first'] == 0:
#                        self.bishoppath()
#                        self.enpass2 = [int((self.ox+self.nx)/2), int((self.oy+self.ny)/2), int((self.oz+self.nz)/2)]
#                    else:
#                        print('Peasants can only double step on their first turn\n')
#                        self.valid = 0
#                elif (self.ny - self.oy == game.turn and self.nz - self.oz == game.turn) and self.dl[0] == 1 and self.dl[1] == 1 and self.dl[2] == 1:
#                    if game.enpass[0] == self.nx and game.enpass[1] == self.ny and game.enpass[2] == self.nz:
#                        for piecetwo in range(len(game.pieces)):
#                            if game.pieces[piecetwo].atr['moved_last_turn'] == True:
#                                self.capture = 1
#                                break
#                    else:
#                        print('Peasants can only move on three dimensional diagonals to capture\n')
#                        self.valid = 0
#                else:
#                    print('This is not a valid location\n')
#                    self.valid = 0
#
#        if self.piece.atr['typ'] == 'soldier':
#            if (self.dx > 1 or self.dy > 1 or self.dz > 1):
#                print('This is not a valid location\n')
#                return 0
#
        if self.piece.piece_type == 'knight':
            if not self.knight_path((1,2)):
                print('This is not a valid location\n')
                return False

        if self.piece.piece_type == 'horse':
            if not self.knight_path((1,1,2)):
                print('This is not a valid location\n')
                return False

        if self.piece.piece_type == 'elephant':
            if not self.knight_path((1,2,2)):
                print('This is not a valid location\n')
                return False

        if self.piece.piece_type == 'rook':
            if not self.queen_path({1}):
                print('This is not a valid location\n')
                return False

        if self.piece.piece_type == 'bishop':
            if not self.queen_path({2}):
                print('This is not a valid location\n')
                return False

        if self.piece.piece_type == 'cardinal':
            if not self.queen_path({3}):
                print('This is not a valid location\n')
                return False

        if self.piece.piece_type == 'queen':
            if not self.queen_path({1,2}):
                print('This is not a valid location\n')
                return False

        if  self.piece.piece_type == 'duchess':
            if not self.queen_path({1,3}):
                print('This is not a valid location\n')
                return False

        if  self.piece.piece_type == 'princess':
            if not self.queen_path({2,3}):
                print('This is not a valid location\n')
                return False

        if  self.piece.piece_type == 'pope':
            if not self.queen_path({1,2,3}):
                print('This is not a valid location\n')
                return False

        if self.capture == True:
            if self.piece.colour == 0:
                capture_position = self.game.next_captured_pos_black
            if self.piece.colour == 1:
                capture_position = self.game.next_captured_pos_white

            self.game.move_piece(self.new_position, capture_position, 'capture')

            # Finding where the next captured piece goes below the board
#            if move2.piece.atr['col'] == 1:
#                game.capturedposg = game.capturedposw
#            if move2.piece.atr['col'] == -1:
#                game.capturedposg = game.capturedposb
#            move2.nx = game.capturedposg%8 + 1
#            if move2.piece.atr['col'] == 1:
#                move2.ny = -((game.capturedposg//8)%4)+8
#            if move2.piece.atr['col'] == -1:
#                move2.ny = ((game.capturedposg//8)%4)+1
#            move2.nz = -(game.capturedposg//32)-1
#            if move2.piece.atr['col'] == 1:
#                game.capturedposw = game.capturedposw + 1
#                game.write(f'{home}/public/misc.txt',None,str(game.capturedposw),1)
#                capturer = ('black')
#                captured = ('white')
#            if move2.piece.atr['col'] == -1:
#                game.capturedposb = game.capturedposb + 1
#                game.write(f'{home}/public/misc.txt',None,str(game.capturedposb),2)
#                capturer = ('white')
#                captured = ('black')
#            game.write(f'{home}/public/pieces.txt',None,f'[{move2.piece.atr["typ"]},({move2.piece.atr["pos"][0]},{move2.piece.atr["pos"][1]},{move2.piece.atr["pos"][2]}),{move2.piece.atr["col"]},{move2.piece.atr["first"]},{move2.piece.atr["moved_last_turn"]}]',move2.term)

            #if game.pieces[piecetwo].atr['typ'] == 'king':
                #print(f'Game over, {capturer} wins!!')
                #game.gameover = 2
                #game.write(f'{home}/public/misc.txt',None,str(game.gameover),5)
                #print('Do you want to play again? (y/n)')

#        if self.piece.atr['typ'] == 'pawn' or self.piece.atr['typ'] == 'peasant':
#            if self.ny == 4+game.turn*4 and self.nz == 4+game.turn*4:
#                self.pro()

        #if move.castlingvar == False:
        return True

#            for u in range(len(game.pieces)):
#                if game.pieces[u].atr['moved_last_turn'] == True:
#                    game.pieces[u].atr['moved_last_turn'] = False
#                    app.rendersi(game.pieces[u].atr,'piece')
#            move.piece.atr['moved_last_turn'] = True
#            try:
#                move.move3.piece.atr['moved_last_turn'] = True
#                app.rendersi(move.move3.piece.atr,'piece')
#            except:
#                pass

#            app.rendersi(self.piece,'piece')
#            game.write(f'{home}/public/misc.txt',None,str(game.turn),0)
#            game.moved_from_last_turn = [self.ox,self.oy,self.oz]
#            game.write(f'{home}/public/misc.txt','moved_from_last_turn: ',f'({game.moved_from_last_turn[0]},{game.moved_from_last_turn[1]},{game.moved_from_last_turn[2]})',3)
#            game.enpass = self.enpass2
#            game.write(f'{home}/public/misc.txt','enpass: ',f'({game.enpass[0]},{game.enpass[1]},{game.enpass[2]})',4)
#            move.move3 = None

    def castling(self):
        ## Queen side vs King side castling
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

    def queen_path(self, dimensions):
        ## Check if the move is only in the exact number of dimesions
        if not len(self.sorted_distance) in dimensions:
            print(dimensions)
            return False

        ## Check if the move is in a straight line
        elif len(set(self.sorted_distance)) != 1:
            print(set(self.sorted_distance))
            print(len(set(self.sorted_distance)))
            return False

        else:
            return True

        ## Check for collisions
        # To complete
        # Figure out direction
        #for u in range (1, self.sorted_distance[0]):
            #square = min(self.new_position, self.old_position)
            #if board[self.] != None

    def knight_path(self, distances):
        if self.sorted_distance == distances:
            return True
        else:
            return False



