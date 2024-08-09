from panda3d.core import *

from math import *

class camera():
    def __init__(self,game_size,game_size_multiplier):

        ## How big the game board is
        self.game_size = game_size
        self.game_size_multiplier = game_size_multiplier

        
        ## The time since the last camera update
        self.time_at_last_update = 0

    def init_white(self):

        ## How far up or down the camera is tilted
        self.pitch = pi/2

        ## How far left or right the camera is tilted
        self.yaw = -pi/2

        ## How far left or right the camera is
        self.x_pos = -30

        ## How far up or down the camera is
        self.y_pos = 22.5

        ## How far in or out the camera is
        self.z_pos = 22.5

        self.update_camera()

    def init_black(self):

        ## How far up or down the camera is tilted
        self.pitch = pi/2

        ## How far left or right the camera is tilted
        self.yaw = pi/2

        ## How far left or right the camera is
        self.x_pos = 75

        ## How far up or down the camera is
        self.y_pos = 22.5

        ## How far in or out the camera is
        self.z_pos = 22.5

        self.update_camera()

    def update_camera(self):

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
        self.y_pos = self.y_pos+distance
        self.check_distance_away()

    def move_down(self,distance):
        self.y_pos = self.y_pos-distance
        self.check_distance_away()

    def move_forward(self,distance):
        self.z_pos = self.z_pos-cos(self.yaw)*distance
        self.x_pos = self.x_pos-sin(self.yaw)*distance
        self.check_distance_away()

    def move_back(self,distance):
        self.z_pos = self.z_pos+cos(self.yaw)*distance
        self.x_pos = self.x_pos+sin(self.yaw)*distance
        self.check_distance_away()

    def move_left(self,distance):
        self.x_pos = self.x_pos-cos(self.yaw)*distance
        self.z_pos = self.z_pos+sin(self.yaw)*distance
        self.check_distance_away()

    def move_right(self,distance):
        self.x_pos = self.x_pos+cos(self.yaw)*distance
        self.z_pos = self.z_pos-sin(self.yaw)*distance
        self.check_distance_away()

    def pitch_up(self,distance):
        if self.pitch > 0:
            self.pitch = self.pitch-distance*pi/32

    def pitch_down(self,distance):
        if self.pitch < pi:
            self.pitch = self.pitch+distance*pi/32

    def yaw_right(self,distance):
        self.yaw = self.yaw+distance*pi/32

    def yaw_left(self,distance):
        self.yaw = self.yaw - distance*pi/32

    def check_distance_away(self):
        max_distance = 28*self.game_size+self.game_size_multiplier
        if sqrt(self.x_pos**2+self.y_pos**2+self.z_pos**2) > max_distance:
            self.init_white()



def create_matrix(i,j,k,l):
    matrix = LMatrix4f()
    matrix.setRow(0,i)
    matrix.setRow(1,j)
    matrix.setRow(2,k)
    matrix.setRow(3,l)
    return matrix

