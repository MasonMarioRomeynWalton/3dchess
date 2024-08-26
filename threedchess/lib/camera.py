from panda3d.core import LVecBase4f, LMatrix4f

from math import *

class controlable_camera():
    def __init__(self,game_size,game_size_multiplier):

        ## How big the game board is
        self.game_size = game_size
        self.game_size_multiplier = game_size_multiplier
        
        ## How far up or down the camera is tilted
        self.pitch = 0

        ## How far left or right the camera is tilted
        self.yaw = 0

        ## How far left or right the camera is
        self.x_pos = 0

        ## How far up or down the camera is
        self.y_pos = 0

        ## How far in or out the camera is
        self.z_pos = 0
        
        ## The time since the last camera update
        self.time_at_last_update = 0

    def init_white(self):
        """
        Initializes the camera for the white player
        """

        self.pitch = pi/2
        self.yaw = -pi/2
        self.x_pos = -30
        self.y_pos = 22.5
        self.z_pos = 22.5

        self.update_camera()

    def init_black(self):
        """
        Initializes the camera for the black player
        """

        self.pitch = pi/2
        self.yaw = pi/2
        self.x_pos = 75
        self.y_pos = 22.5
        self.z_pos = 22.5

        self.update_camera()

    def init_center(self):
        """
        Initializes the camera for the center
        """

        self.pitch = 0
        self.yaw = 0
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0

        self.update_camera()


    def update_camera(self):
        """
        Updates the camera position and orientation
        """

        ## Create the rows of the matrix
        i = LVecBase4f()
        i.set(1,0,0,0)

        j = LVecBase4f()
        j.set(0,cos(self.pitch),-sin(self.pitch),0)

        k = LVecBase4f()
        k.set(0,sin(self.pitch),cos(self.pitch),0)

        l = LVecBase4f()
        l.set(0,0,0,1)

        y_axis_matrix = create_matrix(i,j,k,l)


        ## Create the second matrix
        i = LVecBase4f()
        i.set(cos(self.yaw),0,-sin(self.yaw),0)

        j = LVecBase4f()
        j.set(0,1,0,0)

        k = LVecBase4f()
        k.set(sin(self.yaw),0,cos(self.yaw),0)

        l = LVecBase4f()
        l.set(0,0,0,1)

        x_axis_matrix = create_matrix(i,j,k,l)

        ## Create the multiplication matrix
        matrix = LMatrix4f()
        matrix.multiply(y_axis_matrix,x_axis_matrix)

        ## Set the new matrix
        base.camera.setMat(matrix)
        base.camera.setPos(self.x_pos,self.y_pos,self.z_pos)

    def move_up(self,distance):
        """
        Moves the camera upwards by the given distance

        Args:
            distance (float): How far to move the camera upwards
        """

        self.y_pos = self.y_pos+distance
        self.check_distance_away()

    def move_down(self,distance):
        """
        Moves the camera downwards by the given distance

        Args:
            distance (float): How far to move the camera downwards
        """

        self.y_pos = self.y_pos-distance
        self.check_distance_away()

    def move_forward(self,distance):
        """ Moves the camera forward by the given distance

        Args:
            distance (float): How far to move the camera forward
        """

        self.z_pos = self.z_pos-cos(self.yaw)*distance
        self.x_pos = self.x_pos-sin(self.yaw)*distance
        self.check_distance_away()

    def move_backward(self,distance):
        """Moves the camera backwards by the given distance

        Args:
            distance (float): How far to move the camera backwards
        """

        self.z_pos = self.z_pos+cos(self.yaw)*distance
        self.x_pos = self.x_pos+sin(self.yaw)*distance
        self.check_distance_away()

    def move_left(self,distance):
        """Moves the camera left by the given distance

        Args:
            distance (float): How far to move the camera left
        """

        self.x_pos = self.x_pos-cos(self.yaw)*distance
        self.z_pos = self.z_pos+sin(self.yaw)*distance
        self.check_distance_away()

    def move_right(self,distance):
        """Moves the camera right by the given distance

        Args:
            distance (float): How far to move the camera right
        """

        self.x_pos = self.x_pos+cos(self.yaw)*distance
        self.z_pos = self.z_pos-sin(self.yaw)*distance
        self.check_distance_away()

    def tilt_up(self,distance):
        """Tilts the camera up by the given distance

        Args:
            distance (float): How far to tilt the camera up
        """

        if self.pitch > 0:
            self.pitch = self.pitch-distance*pi/32

    def tilt_down(self,distance):
        """Tilts the camera down by the given distance

        Args:
            distance (float): How far to tilt the camera down
        """

        if self.pitch < pi:
            self.pitch = self.pitch+distance*pi/32

    def pan_left(self,distance):
        """Pans the camera right by the given distance

        Args:
            distance (float): How far to pan the camera right
        """

        self.yaw = self.yaw+distance*pi/32

    def pan_right(self,distance):
        """Pans the camera left by the given distance

        Args:
            distance (float): How far to pan the camera left
        """

        self.yaw = self.yaw - distance*pi/32

    def check_distance_away(self):
        """Checks if the camera is too far away

        Checks if the camera is too far away from the center of the board
        and if so, resets it

        """
        distance = sqrt(self.x_pos**2+self.y_pos**2+self.z_pos**2)
        max_distance = 28*self.game_size+self.game_size_multiplier
        if distance > max_distance:
            self.init_white()



def create_matrix(i,j,k,l):
    """Creates a matrix from the given rows

    Args:
        i (LVecBase4f): First row
        j (LVecBase4f): Second row
        k (LVecBase4f): Third row
        l (LVecBase4f): Fourth row

    Returns:
        LMatrix4f: The matrix
    """

    matrix = LMatrix4f()
    matrix.setRow(0,i)
    matrix.setRow(1,j)
    matrix.setRow(2,k)
    matrix.setRow(3,l)
    return matrix
