from . import move 

def game_help_menu():
    while True:
        print('"p" to get rules for the different pieces')
        print('"m" to see rules for special moves')
        print('Or, input a movement command')

        h = input()

        if h == 'p':
            while True:
                print('"w" to return to the previous menu')
                print('Or enter the piece you want more information about')
                print('Here is a list of pieces:')
                print('king, pawn, peasant, soldier, knight, horse, elephant, rook, bishop, cardinal, queen, duchess, princess, pope')
                h = input()
                print('')
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
                            print('The turn directly after a pawn makes it\'s double step, your opponent\'s pawns or peasants may capture the pawn not only in it\'s current location but also move into the square it passed through during it\'s double step to capture it\n')
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
                            print('The turn directly after a peasant makes it\'s double step, your opponent\'s pawns or peasants may capture the peasant not only in it\'s current location but also move into the square it passed through during it\'s double step to capture it\n')
                        if h == 'p':
                            print('When a peasant makes it to the other side of the board and the other side of the board vertically you must promote it to any piece except:')
                            print('king, pawn, peasant, soldier\n')
                        if h == 'w':
                            break
                    continue
            continue

def print_controls():
    print('Controls:')
    print('Space to go up')
    print('"z" to go down')
    print('"w" to go foward')
    print('"s" to go back')
    print('"a" to go left')
    print('"d" to go right')
    print('"c" to teleport to white\'s start')
    print('"v" to teleport to black\'s start')
    print('"i" to tilt the camera up')
    print('"k" to tilt the camera down')
    print('"j" to tilt the camera left')
    print('"l" to tilt the camera right')
    print('Left click to select the piece you want to move')
    print('Right click to select the square/piece you want to move to')
    print('Enter to move the selected piece to the selected square')
    print('You may also input movement commands from this menu')
    print('')


# Why is this here?
def restart():
    app.reset()
    app.reset2()
    app.unrenders()
    app.unrendersboard()
    print_controls()
    game.restart()
    app.rendersboard()
    app.renders()

## The class for the menus
class menu:
    def __init__(self, description='', submenus={}, pre_text=None, post_text=None, main_menu=False, list_options=True, is_function=False, function=None):

        ## The description of the menu
        self.description = description

        ## A map of the submenus
        self.submenus = submenus

        ## Text to print before the submenus are listed
        self.pre_text = pre_text

        ## Text to print after the submenus are listed
        self.post_text = post_text

        ## Whether the menu is the main menu
        self.main_menu = main_menu

        ## Whether or not the submenus are listed
        ## For example, if the submenus are just the names of the pieces,
        ## Then they are not listed
        self.list_options = list_options

        ## Whether the menu is a function
        self.is_function = is_function

        ## The function if the menu is a function
        self.function = function

    def open(self):
        if self.pre_text != None:
            print(self.pre_text)

        if self.main_menu == False and self.is_function == False and self.submenus:
            print(f'"q" to go back')

        if self.list_options == True:
            for key in self.submenus.keys():
                if self.submenus[key].description != 'Hidden menu':
                    print(f'"{key}" for {self.submenus[key].description}')

        if self.post_text != None:
            print(self.post_text)


        ## If the game is already over the input will mean something else
        ## The promt is printed elsewhere
        # Doesn't work I don't think
        # Move todo
        if main_menu.game.gameover == 2:
            while True:
                if h == 'y':
                    app.reset()
                    app.reset2()
                    app.unrenders()
                    app.unrendersboard()
                    print_controls()
                    main_menu.game.restart()
                    app.rendersboard()
                    app.renders()
                    break
                if h == 'n':
                    print('Thank you for playing!\n')
                    main_menu.game.gameover = 1
                    break
                else:
                    print('This is not a valid selection\n')
                    h = input()
                    print('')

        ## If the game is not over
        elif self.is_function == True:
            self.function()
        ## If there are no submenus
        elif not self.submenus:
            print('')
        else:
            command = input()
            print('')
            if command == 'q':
                if self.main_menu == True:
                    print('You are already in the main menu')
                    print('You cannot go back from here!')
                    print('')
                    self.open()
                else:
                    return
            elif command in self.submenus.keys():
                self.submenus[command].open()

                ## Open your own menu once they've returned
                # May not be what we want
                self.open()
            elif self.main_menu == True:
                check_move_input(command)
                self.open()
            else:
                print('This is not a valid selection\n')
                self.open()

def check_move_input(command):
    ## Check length
    if len(command) != main_menu.game.dimensions*2+1:
        print('Wrong number of characters for move input\n')
        return

    ## Check old location
    old_location = alpha_position_to_list(command[:main_menu.game.dimensions])
    if old_location == None:
        return

    ## Check space
    if command[main_menu.game.dimensions] != ' ':
        print(f'Character {str(main_menu.game.dimensions+1)} is incorrect\n')
        return

    ## Check new location
    new_location = alpha_position_to_list(command[main_menu.game.dimensions+1:])
    if new_location == None:
        return
    
    ## If all is good, run move
    move(main_menu.game, old_location, new_location)

## Changes the move input to a list of numbers
def alpha_position_to_list(command_fragment):
    dimensions = len(command_fragment)

    coordinates = [] 
    for i in range(0, dimensions):
        if ord(command_fragment[i]) in range(ord('0'), ord('8')+1):
            coordinates.append(int(command_fragment[i])-1)
        elif ord(command_fragment[i]) in range(ord('a'), ord('h')+1):
            coordinates.append(ord(command_fragment[i])-ord('a'))
        elif ord(command_fragment[i]) in range(ord('A'), ord('H')+1):
            coordinates.append(ord(command_fragment[i])-ord('A'))
        else:
            print(f'Character {str(i+1)} is incorrect\n')
            return None

    if dimensions == 2:
        coordinates = [coordinates[1], coordinates[0]]

    if dimensions == 3:
        coordinates = [coordinates[1], coordinates[2], coordinates[0]]


    return tuple(coordinates)

help_menu = menu(
    'Hidden menu',
    post_text = (
        '''When I was younger so much younger than today'''
        '''I never needed anybody's help in any way'''
        '''But now these days are gone, I'm not so self assured'''
        '''Now I find I've changed my mind and opened up the doors'''
        '''Uh... You wanted a menu that helps gameplay? Nevermind this then. Press "h" to acess the other help menu'''
    )
)

controls = menu(
    'basic controls',
    is_function = True,
    function = print_controls
)

input_movement_commands = menu(
    'instructions on how to input movement commands from the command line',
    post_text = (
        'Input should be the coordinates of the thing you want to move,\n'
        'a space,'
        'then the coordinates of where you want to move it to.\n'
        'Coordinates are written as a n digit number where n in the number of dimensions\n'
        'Letters can able be used as an alternative to numbers\n'
        'ex: a7u c5u'
    )
)

move_rules = menu(
   'rules on moving pieces', 
    post_text = (
        'You must move one piece per turn\n'
        'After you move, it is your opponent\'s turn\n'
        'Pieces may move based on their move rules (see move rules)\n'
        'Most pieces, with a few notable exceptions, may not move through squares with pieces already in them\n'
        'You may not move pieces into squares you already have pieces in\n'
        'If you move into a square with one of your opponent\'s pieces, then that piece is captured (see capturing)'
    )
)


capture_rules = menu(
    'rules on capturing pieces',
    post_text = (
        'You may move into squares with one of your opponent\'s pieces\n'
        'If you do so, then your opponent\'s piece has been captured\n'
        'Captured pieces are taken off the board and are no longer in the game\n' 
        'If you capture your opponent\'s king, the game is over and you have won (see winning the game)'
    )
)

winning_the_game = menu(
    'how to win the game',
    post_text = (
        'The goal of the game is to capture your opponent\'s king\n'
        'Once a king has been captured, the game is over\n'
        'If your opponent\'s king is captured, you win the game!\n'
        'If your king is captured, you lose the game\n'
        'Note that this version of chess does not have check, a rule used in traditional chess'
    )
)

basic_chess_rules = menu(
    'basic chess rules',
    {
        'm': move_rules,
        'c': capture_rules,
        'w': winning_the_game
    },
    'Basic chess rules menu'
)

# Completely redo this so the piece menu information is stored when we actually create the
# piece is code then use that for these menus
king_description = menu(
    post_text = 'Two cones with a cross on top'
)

pawn_description = menu(
    post_text = 'A cone with a sphere on top'
)

peasant_description = menu(
    post_text = 'A cone with a sphere and hat on top holding a pitchfork'
)

soldier_description = menu(
    post_text = 'A cone with a sphere and helmet on top holding a sword'
)

knight_description = menu(
    post_text = 'A cone and cylinder with a cube and cylinder on top. Spheres for eyes. Looks like a horse'
)

horse_description = menu(
    post_text = 'A cone with a helmet on top and conical pole. Looks like a knight'
)

elephant_description = menu(
    post_text = 'A cone with a sphere on top. Spheres for eyes, cones for tusks, cylinder for trunk'
)

rook_description = menu(
    post_text = 'A cylinder with a hollow cylinder on top. Looks like a castle'
)

bishop_description = menu(
    post_text = 'A cone with a semi-sphere, cone and small sphere on top'
)

cardinal_description = menu(
    post_text = 'A cone with a ring, semi-sphere and small sphere on top'
)

queen_description = menu(
    post_text = 'A cone with a cylinder, cone and small sphere on top'
)

duchess_description = menu(
    post_text = 'A cone with three cylinders on top'
)

princess_description = menu(
    post_text = 'A cone with three cylinders, two semi-spheres and a small sphere on top'
)

pope_description = menu(
    post_text = 'A cone with a semi-sphere and cross on top'
)

visual_descriptions = menu(
    'visual descriptions of each piece',
    {
        'king': king_description,
        'pawn': pawn_description,
        'peasant': peasant_description,
        'soldier': peasant_description,
        'knight': knight_description,
        'horse': horse_description,
        'elephant': elephant_description,
        'rook': rook_description,
        'bishop': bishop_description,
        'cardinal': cardinal_description,
        'queen': queen_description,
        'duchess': duchess_description,
        'princess': princess_description,
        'pope': pope_description
    },
    'Visual descriptions of each piece',
    (
        'Or enter the piece you want a visual description of\n'
        'Here is a list of pieces:\n'
         # Make this procedural
         # No need to gatekeep the other ones though
        'king, pawn, peasant, soldier, knight, horse, elephant, rook, bishop, cardinal, queen, duchess, princess, pope'
    ),
    list_options = False
)

castling_rules = menu(
    'rules for castling',
    post_text = (
        'To castle move your king two squares to the right or left and your rook will move to the square your king passed through\n'
        'In order to castle, neither king nor rook can have moved yet during the game\n'
        'Also note that the rook jumping over the king is the only exception to the rule that the rook may not move through other pieces\n'
        'Another thing to consider is even though some other pieces move like rooks they can still not be used for castling\n'
    )
)

king_rules = menu(
    (
        'The king can move one square in any direction including all diagonals\n'
        'To see the rules for winning the game, see basic chess rules\n'
    ),
    {
        'c': castling_rules
    },
    post_text = 'Note that this 3d version does not have check, a rule used in traditional chess'

)

pawn_rules = None

peasant_rules = None

soldier_rules = menu(
    post_text = (
        'A soldier can move one square in any direction including all diagonals\n'
    )
)

knight_rules = menu(
    post_text = (
        'A knight can move two squares in one direction and one square in a second direction\n'
        'Knights can also jump over (move through) pieces\n'
    )
)

horse_rules = menu(
    post_text = (
        'A horse can move one square in two directions and two squares in a third direction\n'
        'Horses can also jump over (move through) pieces\n'
    )
)

elephant_rules = menu(
    post_text = (
        'An elephant can move two squares in two directions and one square in a third direction\n'
        'Elephants can also jump over (move through) pieces\n'
    )
)

rook_rules = menu(
    post_text = (
        'A rook can move any number of squares in one direction\n'
    )    
)

bishop_rules = menu(
    post_text = (
        'A bishop can move diagonally any number of squares in two directions and zero squares in a third direction\n'
        'Another way to think about it, is that the distance traveled in two directions must be the same, and the distance traveled in the third direction must be zero\n'
        'For example, a bishop could move from one corner of a 2-dimensional board to the opposite corner\n'
        'Hint: Bishops can only move along either the dark squares or the light squares'
    )
)

cardinal_rules = menu(
    post_text = (
        'A cardinal can move diagonally any number of squares in three directions\n'
        'Another way to think about it, is that the distance traveled in all three directions must be the same\n'
        'For example, a cardinal could move from one corner of a 3-dimensional board to the opposite corner\n'
        'Hint: Cardinals can only move along one colour of square (monochrome, blue, red, yellow)'
    )
)

queen_rules = menu(
    post_text = (
        'A queen may either move as a rook or a bishop\n'
        'See rules for those pieces for more details'
    )
)

duchess_rules = menu(
    post_text = (
        'A duchess may either move as a rook or a cardinal\n'
        'See rules for those pieces for more details'
    )
)

princess_rules = menu(
    post_text = (
        'A princess may either move as a bishop or a cardinal\n'
        'See rules for those pieces for more details'
    )
)

pope_rules = menu(
    post_text = (
        'A pope may either move as a rook, a bishop or a cardinal\n'
        'See rules for those pieces for more details'
    )
)

piece_rules = menu(
    'rules for the different pieces',
    {
        'king': king_rules,
        'pawn': pawn_rules,
        'peasant': peasant_rules,
        'soldier': peasant_rules,
        'knight': knight_rules,
        'horse': horse_rules,
        'elephant': elephant_rules,
        'rook': rook_rules,
        'bishop': bishop_rules,
        'cardinal': cardinal_rules,
        'queen': queen_rules,
        'duchess': duchess_rules,
        'princess': princess_rules,
        'pope': pope_rules
    },
    'Rules for the different pieces',
    (
        'Or enter the piece you want rules for\n'
        'Here is a list of pieces:\n'
        'king, pawn, peasant, soldier, knight, horse, elephant, rook, bishop, cardinal, queen, duchess, princess, pope'
    ),
    list_options = False
)

# Maybe add links to these menus
special_moves = menu(
    'rules for special moves',
    post_text = (
        'There are a few special moves to look out for\n'
        'To see castling, go to the king movement rules\n'
        'Note that this 3d version does not have check, a rule used in traditional chess\n'
        'To see pawn double step or pawn promotion, go to the pawn movement rules\n'
        'To see peasant double step or peasant promotion, go to the peasant movement rules\n'
        'To see en passant, go to either the pawn or peasant movement rules'
    ),
    list_options = False
)

game_help = menu(
    'the help menu',
    {
        'c': controls,
        'k': input_movement_commands,
        'b': basic_chess_rules,
        'v': visual_descriptions,
        'p': piece_rules,
        'm': special_moves
    },
    'Welcome to the help menu'
)

restart = menu(
    'restarting the game',
    post_text = 'Restarting the game...',
    is_function = True,
    function = restart
)

main_menu = menu(
    'The main menu',
    {
        'help': help_menu,
        'help!': help_menu,
        'h': game_help,
        'r': restart
    },
    'Enter:',
    'Or enter your move',
    main_menu=True
)

