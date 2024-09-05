class command_line_task():
    def __init__(self, app, game):
        self.app = app
        self.game = game
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
                        app.unrenders()
                        app.unrendersboard()
                        self.print_controls()
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
                app.unrenders()
                app.unrendersboard()
                self.print_controls()
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
                self.print_controls()
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

    def print_controls(self):
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

    def parse(self,h):
        if h[0] == 'a':
            ox = 1
        if h[0] == 'b':
            ox = 2
        if h[0] == 'c':
            ox = 3
        if h[0] == 'd':
            ox = 4
        if h[0] == 'e':
            ox = 5
        if h[0] == 'f':
            ox = 6
        if h[0] == 'g':
            ox = 7
        if h[0] == 'h':
            ox = 8
        oy = int(h[1])
        if h[2] == 's':
            oz = 1
        if h[2] == 't':
            oz = 2
        if h[2] == 'u':
            oz = 3
        if h[2] == 'v':
            oz = 4
        if h[2] == 'w':
            oz = 5
        if h[2] == 'x':
            oz = 6
        if h[2] == 'y':
            oz = 7
        if h[2] == 'z':
            oz = 8
        if h[4] == 'a':
            nx = 1
        if h[4] == 'b':
            nx = 2
        if h[4] == 'c':
            nx = 3
        if h[4] == 'd':
            nx = 4
        if h[4] == 'e':
            nx = 5
        if h[4] == 'f':
            nx = 6
        if h[4] == 'g':
            nx = 7
        if h[4] == 'h':
            nx = 8
        ny = int(h[5])
        if h[6] == 's':
            nz = 1
        if h[6] == 't':
            nz = 2
        if h[6] == 'u':
            nz = 3
        if h[6] == 'v':
            nz = 4
        if h[6] == 'w':
            nz = 5
        if h[6] == 'x':
            nz = 6
        if h[6] == 'y':
            nz = 7
        if h[6] == 'z':
            nz = 8
