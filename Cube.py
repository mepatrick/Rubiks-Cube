#Rubiks cube attempt 2
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import numpy as np
from math import cos, sin, pi
from heapq import heappush, heappop
import copy
from tkinter import *
from time import sleep

import pygame
from pygame.locals import *
import wave

from OpenGL.GL import *
from OpenGL.GLU import *


#root = Tk()
#canvas = Canvas(width=1200,height=600,bg='black')
#canvas.grid()

class Cube():
    """
    The Cube class makes up the entire cube. Each cube has x amount of cubies.
    The number of cubies is related to the size
    size: if size is 2. the cube will be 2*2*2
    """
    #self.size = 0
    #self.cubies = np.zeros((self.size,self.size,self.size))
    def __init__(self, size):
        print("Cube")
        #"forward" rotation
        self.t = 90 * pi / 180
        self.Rx = np.matrix([[1, 0, 0], [0, cos(self.t), -sin(self.t)], [0, sin(self.t), cos(self.t)]])
        self.Ry = np.matrix([[cos(self.t), 0 , sin(self.t)], [0,1,0], [-sin(self.t),0,cos(self.t)]])
        self.Rz = np.matrix([[cos(self.t),-sin(self.t),0], [sin(self.t),cos(self.t),0], [0,0,1]])
        #"backward" rotation
        self.negT = -90 * pi /180
        self.negRx = np.matrix([[1, 0, 0], [0, cos(self.negT), -sin(self.negT)], [0, sin(self.negT), cos(self.negT)]])
        self.negRy = np.matrix([[cos(self.negT), 0 , sin(self.negT)], [0,1,0], [-sin(self.negT),0,cos(self.negT)]])
        self.negRz = np.matrix([[cos(self.negT),-sin(self.negT),0], [sin(self.negT),cos(self.negT),0], [0,0,1]])
        #not using size right now
        self.size = size
        
        self.coords = [-1,1]
        self.cubies = [[[0 for i in range(self.size)] for j in range(self.size)] for k in range(self.size)]
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    self.cubies[x][y][z] = Cubie(self.coords[x],self.coords[y],self.coords[z])

    #need this because heap was comparing Cube objects
    def __lt__(self, other):
        return 0

    def rotateX(self,index,direction):
        """
        index: either 0 or 1 (left or right side of cube)
        direction: rotation clockwise (1) or counter clockwise (-1)
        """
        for row in self.cubies:
            for row2 in row:
                for cubie in row2:
                    #print(cubie.x,cubie.y,cubie.z)
                    if cubie.x == index:
                        cord = np.matrix([[cubie.x],[cubie.y],[cubie.z]])
                        #rotate specific direction
                        if direction == 1:
                            new_cord = self.Rx.dot(cord)
                            #cubie.update(round(new_cord[0, 0]),round(new_cord[1, 0]), round(new_cord[2, 0]))
                        else:
                            new_cord = self.negRx.dot(cord)
                        cubie.update(round(new_cord[0, 0]),round(new_cord[1, 0]), round(new_cord[2, 0]),index,direction,'x')

    def rotateY(self,index,direction):
        for row in self.cubies:
            for row2 in row:
                for cubie in row2:
                    #print(cubie.x,cubie.y,cubie.z)
                    if cubie.y == index:
                        cord = np.matrix([[cubie.x],[cubie.y],[cubie.z]])
                        if direction == 1:
                            new_cord = self.Ry.dot(cord)
                            #cubie.update(round(new_cord[0, 0]),round(new_cord[1, 0]),round(new_cord[2, 0]))
                        else:
                            new_cord = self.negRy.dot(cord)
                        cubie.update(round(new_cord[0, 0]),round(new_cord[1, 0]),round(new_cord[2, 0]),index,direction,'y')


    def rotateZ(self,index,direction):
        for row in self.cubies:
            for row2 in row:
                for cubie in row2:
                    #print(cubie.x,cubie.y,cubie.z)
                    if cubie.z == index:
                        cord = np.matrix([[cubie.x],[cubie.y],[cubie.z]])
                        if direction == 1:
                            new_cord = self.Rz.dot(cord)
                            #cubie.update(round(new_cord[0, 0]),round(new_cord[1, 0]),round(new_cord[2, 0]))
                        else:
                            new_cord = self.negRz.dot(cord)
                        cubie.update(round(new_cord[0, 0]),round(new_cord[1, 0]),round(new_cord[2, 0]),index,direction,'z')        
                        
    def draw(self):
        for row in self.cubies:
            for row2 in row:
                for cubie in row2:
                    cubie.draw_cubie()
        
                    

class Cubie():
    """
    x: the x position of the cubie
    y: the y position of the cubie
    z: the z position of the cubie
    """
    def __init__(self, x, y, z):
        #print("Cubie")
        #self.draw_postions = {(1,1,1):{'white':(4,1)
        self.x = x
        self.y = y
        self.z = z
        self.t = 90 * pi / 180
        self.negT = -90 * pi /180
        #self.True_Face_Values = {'white':[0,1,0],'red':[0,0,-1],'green':[1,0,0],'blue':[0,0,1],'yellow':[-1,0,0],'orange':[0,-1,0]} #tells you where each face SHOULD be
        #self.Faces = {'white':[0,1,0],'red':[0,0,-1],'green':[1,0,0],'blue':[0,0,1],'yellow':[-1,0,0],'orange':[0,-1,0]}#tells you where each face is

        self.Faces = {(1,1,1):[0,1,0],(1,0,0):[0,0,-1],(0,1,0):[1,0,0],(0,0,1):[0,0,1],(1,1,0):[-1,0,0],(1,.5,0):[0,-1,0]}
        self.True_Face_Values = {(1,1,1):[0,1,0],(1,0,0):[0,0,-1],(0,1,0):[1,0,0],(0,0,1):[0,0,1],(1,1,0):[-1,0,0],(1,.5,0):[0,-1,0]}
        
        self.vertices = self.gen_cords((self.x,self.y,self.z),1)
        self.edges = (
            (0,1),
            (0,2),
            (0,4),
            (2,6),
            (2,3),
            (1,3),
            (1,5),
            (4,5),
            (4,6),
            (7,6),
            (7,5),
            (7,3)
            )
        self.surfaces = (
            (4,0,2,6), # back
            (0,2,3,1), # right
            (5,1,3,7), # front
            (4,5,7,6), # left
            (4,0,1,5), # top
            (6,2,3,7)  # bottom
            )
        self.colors = {
            (4,0,2,6):[(0,1,1),[0,0,1]],
            (0,2,3,1):[(1,0,0),[1,0,0]],
            (5,1,3,7):[(0,1,0),[0,0,-1]],
            (4,5,7,6):[(0,0,1),[-1,0,0]],
            (4,0,1,5):[(1,1,0),[0,1,0]],
            (6,2,3,7):[(1,0,1),[0,-1,0]]}
        
    def update(self, x, y, z,index,direction,axis):
        #not using index, will remove later
        self.x = x
        self.y = y
        self.z = z

        if axis == 'x':
            self.rotate_face_x(direction)
        elif axis == 'y':
            self.rotate_face_y(direction)
        else:
            self.rotate_face_z(direction)
        self.vertices = self.gen_cords((self.x,self.y,self.z),1)

    def rotate_face_x(self,direction):
        for value in self.Faces.items():
            color,vector = value
            if direction == 1:
                angle = self.t
            else:
                angle = self.negT
            x = vector[0]
            y = round(vector[1] * cos(angle) - vector[2] * sin(angle))
            z = round(vector[1] * sin(angle) + vector[2] * cos(angle))
            vector[1] = y
            vector[2] = z

    def rotate_face_y(self,direction):
        for value in self.Faces.items():
            color,vector = value
            if direction == 1:
                angle = self.t
            else:
                angle = self.negT
            y = vector[1]
            x = round(vector[0] * cos(angle) - vector[2] * sin(angle))
            z = round(vector[0] * sin(angle) + vector[2] * cos(angle))
            vector[0] = x
            vector[2] = z

    def rotate_face_z(self,direction):
        #print("Faces: " + str(self.Faces))
        for value in self.Faces.items():
            color,vector = value
            if direction == 1:
                angle = self.t
            else:
                angle = self.negT
            z = vector[2]
            x = round(vector[0] * cos(angle) - vector[1] * sin(angle))
            y = round(vector[0] * sin(angle) + vector[1] * cos(angle))
            vector[0] = x
            vector[1] = y
        #print("New Faces: " + str(self.Faces))

    def draw_cubie(self):
        #print(self.x,self.y,self.z)
        #print(self.vertices)
        
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for face in self.Faces.items():
                if face[1] == self.colors[surface][1]:
                    self.colors[surface][0] = face[0]
            x = 0
            glColor3fv(self.colors[surface][0])
            for vertex in surface:
                x+=1
                glVertex3fv(self.vertices[vertex])
        glEnd()
        
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                
                glVertex3fv(self.vertices[vertex])
        glEnd()        

    def gen_cords(self,c,a):
        #c: center cords
        #a: half the length of square
        x = []
        x.append(c[0]+a)
        x.append(c[0]-a)
        y = []
        y.append(c[1]+a)
        y.append(c[1]-a)
        z = []
        z.append(c[2]+a)
        z.append(c[2]-a)

        cords = []
        for i in x:
            for j in y:
                for k in z:
                    cords.append((i,j,k))
        return cords
        
        

#get the heuristic value of the cube
#should change
def heuristic(cube):
    value = 0
    for row in cube.cubies:
        for row2 in row:
            for cubie in row2:
                if cubie.x == 1 and cubie.Faces[(0,1,0)] != cubie.True_Face_Values[(0,1,0)]: # if the colors on the right side are not green increase the heuristic value
                    value += 1
                if cubie.x == -1 and cubie.Faces[(1,1,0)] != cubie.True_Face_Values[(1,1,0)]: #left side
                    value += 1
                if cubie.y == 1 and cubie.Faces[(1,1,1)] != cubie.True_Face_Values[(1,1,1)]: # top
                    value += 1
                if cubie.y == -1 and cubie.Faces[(1,.5,0)] != cubie.True_Face_Values[(1,.5,0)]: # bottom
                    value += 1
                if cubie.z == 1 and cubie.Faces[(0,0,1)] != cubie.True_Face_Values[(0,0,1)]: # back
                    value += 1
                if cubie.z == -1 and cubie.Faces[(1,0,0)] != cubie.True_Face_Values[(1,0,0)]: # front
                    value += 1
    
    return value

def neighbors(cube):
    #generate deep copy of cube
    #generate all neighbors of a single cube state
    cube_neighbors = []
    for i in range(12):
        new_cube = copy.deepcopy(cube)
        if i == 0:
            new_cube.rotateX(1,1)
        if i == 1:
            new_cube.rotateX(1,-1)
        if i == 2:
            new_cube.rotateX(-1,1)
        if i == 3:
            new_cube.rotateX(-1,-1)
        if i == 4:
            new_cube.rotateY(1,1)
        if i == 5:
            new_cube.rotateY(1,-1)
        if i == 6:
            new_cube.rotateY(-1,1)
        if i == 7:
            new_cube.rotateY(-1,-1)
        if i == 8:
            new_cube.rotateZ(1,1)
        if i == 9:
            new_cube.rotateZ(1,-1)
        if i == 10:
            new_cube.rotateZ(-1,1)
        if i == 11:
            new_cube.rotateZ(-1,-1)
            
        tup = ()
        tup = tup + (1,) # (heuristic(cube),)
        tup = tup + (new_cube,)
        cube_neighbors.append(tup)

    return cube_neighbors

#Next step write function that shuffles cube
def randomize(cube):
    for i in range(1):
        cube.rotateZ(1,-1)
        cube.rotateZ(-1,1)
        cube.rotateX(1,1)
        cube.rotateX(-1,-1)
        #cube.rotateY(1,-1)
        
#Then start with iterative deepening A*
def astar(start,goal,get_neighbors,heuristic,limit):
    info = {start: (0,None)}
    heap = [(0,start,0)]
    while len(heap) > 0:
        value, cube, current_depth = heappop(heap)

        glRotatef(1, 1, 3, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        cube.draw()
        pygame.display.flip()
        pygame.time.wait(10)
        
        if heuristic(cube) == 0: #cube is solved
            path = []
            while cube != None:
                path.append(cube)
                cube = info[cube][1]
            path.reverse()
            return path

        cost = info[cube][0]
        neighbors = get_neighbors(cube)
        #print(neighbors)
        for weight,u in neighbors:#get_neighbors(cube):
            if current_depth < limit-1:
                if u not in info or weight + cost < info[u][0]:
                    info[u] = (weight+cost, cube)
                    heappush(heap, (weight+cost+heuristic(u), u ,current_depth + 1))
        #sleep(.5)

    return []

def iterative_deepening_Astar(start,goal,get_neighbors,heuristic,max_depth):
    i = 1
    while i < max_depth:
        print(i)
        result = astar(start,goal,get_neighbors,heuristic,i)
        if result != []:
            return result
        i += 1
        


def main():
    #print("main")
    pygame.init()
    #sound_file = wave.open("breakout.wav")
    #freq = sound_file.getframerate()
    #print(freq)
    #pygame.mixer.init(frequency=freq)
    #pygame.mixer.music.load("breakout.wav")
    #pygame.mixer.music.play()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)

    gluPerspective(100, (display[0]/display[1]), .1, 50)

    glTranslatef(0.0,0.0, -10)
    
    cube = Cube(2)
    
    goal = copy.deepcopy(cube)
    randomize(cube)
    
    solved_cube = iterative_deepening_Astar(cube,goal,neighbors,heuristic,10)
    print("path length: " + str(len(solved_cube)))
    
    i = 0
    while i < 500:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()
        glRotatef(1, 1, 3, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        solved_cube[-1].draw()
        pygame.display.flip()
        pygame.time.wait(10)
        i += 1

    #Shows the rotations in order to solve the cube
    for cube in solved_cube:
        glRotatef(1, 1, 3, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        cube.draw()
        pygame.display.flip()
        pygame.time.wait(10)
        sleep(.5)


if __name__ == "__main__":
    main()
