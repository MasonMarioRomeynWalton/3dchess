def get_piece_layout(dimensions, size_of_dimensions, unused_dimensions, side_dimensions, across_dimensions):

    ## Layout for 1 dimension
    if dimensions == 1:
        layout = [
            {
                'piece_type': 'king',
                'position': (0,),
            },
            {
                'piece_type': 'king',
                'position': (7,),
            }
        ]

    ## Layout for 2 dimensions
    if dimensions == 2:
        
        layout = [
            {
                'piece_type': 'king',
                'position': (0, 4),
            },
            *[
                {
                    'piece_type': 'pawn',
                    'position': (1, i),
                } for i in range(0, size_of_dimensions[1])
            ],
            {
                'piece_type': 'knight',
                'position': (0, 1),
            },
            {
                'piece_type': 'knight',
                'position': (0, 6),
            },
            {
                'piece_type': 'rook',
                'position': (0, 0),
            },
            {
                'piece_type': 'rook',
                'position': (0, 7),
            },
            {
                'piece_type': 'bishop',
                'position': (0, 2),
            },
            {
                'piece_type': 'bishop',
                'position': (0, 5),
            },
            {
                'piece_type': 'queen',
                'position': (0, 3),
            },
        ]


    ## Layout for 3 dimesions
    if dimensions == 3:
        layout = [
            {
                'piece_type': 'king',
                'position': (0, 0, 4),
                'colour': 0
            },
            *[
                {
                    'piece_type': 'pawn',
                    'position': (1, 2, i),
                    'colour': 0
                } for i in range(0, size_of_dimensions[2])
            ],
            *[
                {
                    'piece_type': 'pawn',
                    'position': (2, 1, i),
                    'colour': 0
                } for i in range(0, size_of_dimensions[2])
            ],
            *[
                {
                    'piece_type': 'peasant',
                    'position': (0, 2, i),
                    'colour': 0
                } for i in range(0, size_of_dimensions[2])
            ],
            *[
                {
                    'piece_type': 'peasant',
                    'position': (2, 0, i),
                    'colour': 0
                } for i in range(0, size_of_dimensions[2])
            ],
            *[
                {
                    'piece_type': 'soldier',
                    'position': (2, 2, i),
                    'colour': 0
                } for i in range(0, size_of_dimensions[2])
            ],
            {
                'piece_type': 'knight',
                'position': (0, 1, 0),
                'colour': 0
            },
            {
                'piece_type': 'knight',
                'position': (1, 1, 3),
                'colour': 0
            },
            {
                'piece_type': 'knight',
                'position': (1, 1, 4),
                'colour': 0
            },
            {
                'piece_type': 'knight',
                'position': (0, 1, 7),
                'colour': 0
            },
            {
                'piece_type': 'horse',
                'position': (1, 1, 0),
                'colour': 0
            },
            {
                'piece_type': 'horse',
                'position': (0, 1, 1),
                'colour': 0
            },
            {
                'piece_type': 'horse',
                'position': (0, 1, 6),
                'colour': 0
            },
            {
                'piece_type': 'horse',
                'position': (1, 1, 7),
                'colour': 0
            },
            {
                'piece_type': 'elephant',
                'position': (1, 0, 0),
                'colour': 0
            },
            {
                'piece_type': 'elephant',
                'position': (1, 1, 1),
                'colour': 0
            },
            {
                'piece_type': 'elephant',
                'position': (1, 1, 6),
                'colour': 0
            },
            {
                'piece_type': 'elephant',
                'position': (1, 0, 7),
                'colour': 0
            },
            {
                'piece_type': 'rook',
                'position': (0, 0, 0),
                'colour': 0
            },
            {
                'piece_type': 'rook',
                'position': (1, 1, 2),
                'colour': 0
            },
            {
                'piece_type': 'rook',
                'position': (1, 1, 5),
                'colour': 0
            },
            {
                'piece_type': 'rook',
                'position': (0, 0, 7),
                'colour': 0
            },
            {
                'piece_type': 'bishop',
                'position': (1, 0, 1),
                'colour': 0
            },
            {
                'piece_type': 'bishop',
                'position': (0, 1, 2),
                'colour': 0
            },
            {
                'piece_type': 'bishop',
                'position': (0, 1, 5),
                'colour': 0
            },
            {
                'piece_type': 'bishop',
                'position': (1, 0, 6),
                'colour': 0
            },
            {
                'piece_type': 'cardinal',
                'position': (0, 0, 1),
                'colour': 0
            },
            {
                'piece_type': 'cardinal',
                'position': (1, 0, 2),
                'colour': 0
            },
            {
                'piece_type': 'cardinal',
                'position': (1, 0, 5),
                'colour': 0
            },
            {
                'piece_type': 'cardinal',
                'position': (0, 0, 6),
                'colour': 0
            },
            {
                'piece_type': 'queen',
                'position': (0, 0, 2),
                'colour': 0
            },
            {
                'piece_type': 'queen',
                'position': (0, 0, 5),
                'colour': 0
            },
            {
                'piece_type': 'duchess',
                'position': (1, 0, 3),
                'colour': 0
            },
            {
                'piece_type': 'duchess',
                'position': (1, 0, 4),
                'colour': 0
            },
            {
                'piece_type': 'princess',
                'position': (0, 1, 3),
                'colour': 0
            },
            {
                'piece_type': 'princess',
                'position': (0, 1, 4),
                'colour': 0
            },
            {
                'piece_type': 'pope',
                'position': (0, 0, 3),
                'colour': 0
            },
        ]

    return layout




    
#self.create_piece('king',    (7, 7, 4), 1)
#self.create_piece_row(
#    'pawn',
#    (self.size_of_dimensions[0]-2, self.size_of_dimensions[1]-3),
#    1
#)
#self.create_piece_row(
#    'pawn',
#    (self.size_of_dimensions[0]-3, self.size_of_dimensions[1]-2),
#    1
#)
#self.create_piece_row(
#    'peasant',
#    (self.size_of_dimensions[0]-1, self.size_of_dimensions[1]-3),
#    1
#)
#self.create_piece_row(
#    'peasant',
#    (self.size_of_dimensions[0]-3, self.size_of_dimensions[1]-1),
#    1
#)
#self.create_piece_row(
#    'soldier',
#    (self.size_of_dimensions[0]-3, self.size_of_dimensions[1]-3),
#    1
#)
#self.create_piece('knight',  (7, 6, 0), 1)
#self.create_piece('knight',  (6, 6, 3), 1)
#self.create_piece('knight',  (6, 6, 4), 1)
#self.create_piece('knight',  (7, 6, 7), 1)
#self.create_piece('horse',   (6, 6, 0), 1)
#self.create_piece('horse',   (7, 6, 1), 1)
#self.create_piece('horse',   (7, 6, 6), 1)
#self.create_piece('horse',   (6, 6, 7), 1)
#self.create_piece('elephant',(6, 7, 0), 1)
#self.create_piece('elephant',(6, 6, 1), 1)
#self.create_piece('elephant',(6, 6, 6), 1)
#self.create_piece('elephant',(6, 7, 7), 1)
#self.create_piece('rook',    (7, 7, 0), 1)
#self.create_piece('rook',    (6, 6, 2), 1)
#self.create_piece('rook',    (6, 6, 5), 1)
#self.create_piece('rook',    (7, 7, 7), 1)
#self.create_piece('bishop',  (6, 7, 1), 1)
#self.create_piece('bishop',  (7, 6, 2), 1)
#self.create_piece('bishop',  (7, 6, 5), 1)
#self.create_piece('bishop',  (6, 7, 6), 1)
#self.create_piece('cardinal',(7, 7, 1), 1)
#self.create_piece('cardinal',(6, 7, 2), 1)
#self.create_piece('cardinal',(6, 7, 5), 1)
#self.create_piece('cardinal',(7, 7, 6), 1)
#self.create_piece('queen',   (7, 7, 2), 1)
#self.create_piece('queen',   (7, 7, 5), 1)
#self.create_piece('duchess', (6, 7, 3), 1)
#self.create_piece('duchess', (6, 7, 4), 1)
#self.create_piece('princess',(7, 6, 3), 1)
#self.create_piece('princess',(7, 6, 4), 1)
#self.create_piece('pope',    (7, 7, 3), 1)
#
#create_piece('king',    (0, 0, 4), 0)
#self.create_piece_row('pawn', (1, 2), 0)
#self.create_piece_row('pawn', (2, 1), 0)
#self.create_piece_row('peasant', (0, 2), 0)
#self.create_piece_row('peasant', (2, 0), 0)
#self.create_piece_row('soldier', (2, 2), 0)
#self.create_piece('knight',  (0, 1, 0), 0)
#self.create_piece('knight',  (1, 1, 3), 0)
#self.create_piece('knight',  (1, 1, 4), 0)
#self.create_piece('knight',  (0, 1, 7), 0)
#self.create_piece('horse',   (1, 1, 0), 0)
#self.create_piece('horse',   (0, 1, 1), 0)
#self.create_piece('horse',   (0, 1, 6), 0)
#self.create_piece('horse',   (1, 1, 7), 0)
#self.create_piece('elephant',(1, 0, 0), 0)
#self.create_piece('elephant',(1, 1, 1), 0)
#self.create_piece('elephant',(1, 1, 6), 0)
#self.create_piece('elephant',(1, 0, 7), 0)
#self.create_piece('rook',    (0, 0, 0), 0)
#self.create_piece('rook',    (1, 1, 2), 0)
#self.create_piece('rook',    (1, 1, 5), 0)
#self.create_piece('rook',    (0, 0, 7), 0)
#self.create_piece('bishop',  (1, 0, 1), 0)
#self.create_piece('bishop',  (0, 1, 2), 0)
#self.create_piece('bishop',  (0, 1, 5), 0)
#self.create_piece('bishop',  (1, 0, 6), 0)
#self.create_piece('cardinal',(0, 0, 1), 0)
#self.create_piece('cardinal',(1, 0, 2), 0)
#self.create_piece('cardinal',(1, 0, 5), 0)
#self.create_piece('cardinal',(0, 0, 6), 0)
#self.create_piece('queen',   (0, 0, 2), 0)
#self.create_piece('queen',   (0, 0, 5), 0)
#self.create_piece('duchess', (1, 0, 3), 0)
#self.create_piece('duchess', (1, 0, 4), 0)
#self.create_piece('princess',(0, 1, 3), 0)
#self.create_piece('princess',(0, 1, 4), 0)
#self.create_piece('pope',    (0, 0, 3), 0)
#
