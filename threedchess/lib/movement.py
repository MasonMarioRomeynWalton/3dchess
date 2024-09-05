class move:
    def __init__(self, old_position, new_position, castling_movement = False):
        self.old_position = old_position
        self.new_position = new_position
        self.distance_between_positions = [
            abs(self.old_position[i] - self.new_position[i]) for i in range(0,3)
        ]

        self.castling_movement = castling_movement

    def findpiece(self):
        piece_found = 0
        for u in range(0,len(game.pieces)):
            if game.pieces[u].atr['pos'][0] == self.ox and game.pieces[u].atr['pos'][1] == self.oy and game.pieces[u].atr['pos'][2] == self.oz:
                self.term = u
                self.piece = game.pieces[u]
                self.process()
                piece_found = 1
        if piece_found == 0:
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

