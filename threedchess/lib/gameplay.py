class game():
    def __init__(self, across_dimensions = 2, side_dimensions = 1, size_of_dimensions = [8,8,8]):
        self.across_dimensions = across_dimensions
        self.side_dimensions = side_dimensions
        self.dimensions = self.across_dimensions + self.side_dimensions

        self.size_of_dimensions = [1,1,1]
        for i in range(0, self.across_dimensions):
            self.size_of_dimensions[i] = size_of_dimensions[i]

        for i in range(0, self.side_dimensions):
            self.size_of_dimensions[-i-1] = size_of_dimensions[-i-1]

    def restart(self):
        ##For starting a game of the same type

        self.turn = 1
        self.capturedposw = None
        self.capturedposb = None
        self.moved_from_last_turn = [None,None,None]
        self.enpass = [None,None,None]
        self.gameover = False

        self.board = self.create_board([0,0,0], 3)

        self.pieces = []

        if self.dimensions == 1:
            self.create_piece(('king',    [0], 0))

            self.create_piece(('king',    [7], 1))

        if self.dimensions == 2:
            
            self.create_piece('king',    [0, 4], 0)
            self.create_piece_row('pawn', [1], 0)
            self.create_piece('knight',  [0, 1], 0)
            self.create_piece('knight',  [0, 6], 0)
            self.create_piece('rook',    [0, 0], 0)
            self.create_piece('rook',    [0, 7], 0)
            self.create_piece('bishop',  [0, 2], 0)
            self.create_piece('bishop',  [0, 5], 0)
            self.create_piece('queen',   [0, 3], 0)

            self.create_piece('king',    [7, 4], 1)
            self.create_piece_row('pawn', [self.size_of_dimensions[0]-2], 1)
            self.create_piece('knight',  [7, 1], 1)
            self.create_piece('knight',  [7, 6], 1)
            self.create_piece('rook',    [7, 0], 1)
            self.create_piece('rook',    [7, 7], 1)
            self.create_piece('bishop',  [7, 2], 1)
            self.create_piece('bishop',  [7, 5], 1)
            self.create_piece('queen',   [7, 3], 1)

        if self.dimensions == 3:
            self.create_piece('king',    [0, 0, 4], 0)
            self.create_piece_row('pawn', [1, 2], 0)
            self.create_piece_row('pawn', [2, 1], 0)
            self.create_piece_row('peasant', [0, 2], 0)
            self.create_piece_row('peasant', [2, 0], 0)
            self.create_piece_row('soldier', [2, 2], 0)
            self.create_piece('knight',  [0, 1, 0], 0)
            self.create_piece('knight',  [1, 1, 3], 0)
            self.create_piece('knight',  [1, 1, 4], 0)
            self.create_piece('knight',  [0, 1, 7], 0)
            self.create_piece('horse',   [1, 1, 0], 0)
            self.create_piece('horse',   [0, 1, 1], 0)
            self.create_piece('horse',   [0, 1, 6], 0)
            self.create_piece('horse',   [1, 1, 7], 0)
            self.create_piece('elephant',[1, 0, 0], 0)
            self.create_piece('elephant',[1, 1, 1], 0)
            self.create_piece('elephant',[1, 1, 6], 0)
            self.create_piece('elephant',[1, 0, 7], 0)
            self.create_piece('rook',    [0, 0, 0], 0)
            self.create_piece('rook',    [1, 1, 2], 0)
            self.create_piece('rook',    [1, 1, 5], 0)
            self.create_piece('rook',    [0, 0, 7], 0)
            self.create_piece('bishop',  [1, 0, 1], 0)
            self.create_piece('bishop',  [0, 1, 2], 0)
            self.create_piece('bishop',  [0, 1, 5], 0)
            self.create_piece('bishop',  [1, 0, 6], 0)
            self.create_piece('cardinal',[0, 0, 1], 0)
            self.create_piece('cardinal',[1, 0, 2], 0)
            self.create_piece('cardinal',[1, 0, 5], 0)
            self.create_piece('cardinal',[0, 0, 6], 0)
            self.create_piece('queen',   [0, 0, 2], 0)
            self.create_piece('queen',   [0, 0, 5], 0)
            self.create_piece('duchess', [1, 0, 3], 0)
            self.create_piece('duchess', [1, 0, 4], 0)
            self.create_piece('princess',[0, 1, 3], 0)
            self.create_piece('princess',[0, 1, 4], 0)
            self.create_piece('pope',    [0, 0, 3], 0)

            self.create_piece('king',    [7, 7, 4], 1)
            self.create_piece_row('pawn', [self.size_of_dimensions[0]-2, self.size_of_dimensions[1]-3], 1)
            self.create_piece_row('pawn', [self.size_of_dimensions[0]-3, self.size_of_dimensions[1]-2], 1)
            self.create_piece_row('peasant', [self.size_of_dimensions[0]-1, self.size_of_dimensions[1]-3], 1)
            self.create_piece_row('peasant', [self.size_of_dimensions[0]-3, self.size_of_dimensions[1]-1], 1)
            self.create_piece_row('soldier', [self.size_of_dimensions[0]-3, self.size_of_dimensions[1]-3], 1)
            self.create_piece('knight',  [7, 6, 0], 1)
            self.create_piece('knight',  [6, 6, 3], 1)
            self.create_piece('knight',  [6, 6, 4], 1)
            self.create_piece('knight',  [7, 6, 7], 1)
            self.create_piece('horse',   [6, 6, 0], 1)
            self.create_piece('horse',   [7, 6, 1], 1)
            self.create_piece('horse',   [7, 6, 6], 1)
            self.create_piece('horse',   [6, 6, 7], 1)
            self.create_piece('elephant',[6, 7, 0], 1)
            self.create_piece('elephant',[6, 6, 1], 1)
            self.create_piece('elephant',[6, 6, 6], 1)
            self.create_piece('elephant',[6, 7, 7], 1)
            self.create_piece('rook',    [7, 7, 0], 1)
            self.create_piece('rook',    [6, 6, 2], 1)
            self.create_piece('rook',    [6, 6, 5], 1)
            self.create_piece('rook',    [7, 7, 7], 1)
            self.create_piece('bishop',  [6, 7, 1], 1)
            self.create_piece('bishop',  [7, 6, 2], 1)
            self.create_piece('bishop',  [7, 6, 5], 1)
            self.create_piece('bishop',  [6, 7, 6], 1)
            self.create_piece('cardinal',[7, 7, 1], 1)
            self.create_piece('cardinal',[6, 7, 2], 1)
            self.create_piece('cardinal',[6, 7, 5], 1)
            self.create_piece('cardinal',[7, 7, 6], 1)
            self.create_piece('queen',   [7, 7, 2], 1)
            self.create_piece('queen',   [7, 7, 5], 1)
            self.create_piece('duchess', [6, 7, 3], 1)
            self.create_piece('duchess', [6, 7, 4], 1)
            self.create_piece('princess',[7, 6, 3], 1)
            self.create_piece('princess',[7, 6, 4], 1)
            self.create_piece('pope',    [7, 7, 3], 1)

        for piece in self.pieces:
            related_board = self.board.copy()
            for dimension in range(2, -1, -1):
                related_board = related_board[piece.position[dimension]]

        #
        return
        #

        self.create(f'{home}/public/pieces.txt',len(self.pieces))
        self.create(f'{home}/public/misc.txt',6)

        self.save = []
        for u in range(0,len(self.pieces)):
            self.save.append(self.pieces[u].atr['typ']+': '+f'[{self.pieces[u].atr["typ"]},({self.pieces[u].atr["pos"][0]},{self.pieces[u].atr["pos"][1]},{self.pieces[u].atr["pos"][2]}),{self.pieces[u].atr["col"]},{self.pieces[u].atr["first"]},{self.pieces[u].atr["moved_last_turn"]}]'+'\n')
        self.writer = open(f'{home}/public/pieces.txt', 'w')
        self.writer.writelines(self.save)
        self.writer.close()
        self.write(f'{home}/public/misc.txt','turn: ',str(self.turn),0)
        self.write(f'{home}/public/misc.txt','capturedposw: ',str(self.capturedposw),1)
        self.write(f'{home}/public/misc.txt','capturedposb: ',str(self.capturedposb),2)
        self.write(f'{home}/public/misc.txt','moved_from_last_turn: ',f'({self.moved_from_last_turn[0]},{self.moved_from_last_turn[1]},{self.moved_from_last_turn[2]})',3)
        self.write(f'{home}/public/misc.txt','enpass: ',f'({self.enpass[0]},{self.enpass[1]},{self.enpass[2]})',4)
        self.write(f'{home}/public/misc.txt','gameover: ',str(self.gameover),5)

    def create_piece_row(self, piece_type, position, colour):
        for i in range(0, self.size_of_dimensions[-1]): 
            self.create_piece(piece_type, position+[i], colour)

    def create_piece(self, piece_type, position, colour):
        full_position = [0,0,0]
        for i in range(0, self.across_dimensions):
            full_position[i] = position[i]

        for i in range(0, self.side_dimensions):
            full_position[-i-1] = position[-i-1]

        piece = game_piece(piece_type, full_position, colour)
        self.pieces.append(piece)



    def create_board(self, pos, dimensions):
        if dimensions == 0:
            return None
        else:
            board = []
            for sub_board in range(0,self.size_of_dimensions[dimensions-1]):
                sub_board_pos = pos.copy()
                sub_board_pos[dimensions-1] = sub_board
                board.append(self.create_board(pos, dimensions-1))

            return board



    def open(self):
        read.print_controls()

        self.pieces = []
        self.reader = open(f'{home}/public/pieces.txt','r')
        self.save = self.reader.readlines()
        for u in range(0,len(self.save)-1):
            self.pieces.append('')
            self.sp = self.split(self.save[u])
            self.pieces[u] = piecec(self.sp[0],self.sp[1],self.sp[2])
            self.pieces[u].has_moved= self.sp[3]
            self.pieces[u].moved_last_turn = self.sp[4]
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

class game_piece:
    def __init__(self,piece_type,position,colour):
        self.piece_type = piece_type
        self.position = position
        self.colour = colour
        self.has_moved = False
        self.moved_last_turn = False
