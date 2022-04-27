import numpy as np
import random
from  errors import DirectionNotFoundError, CommandDoesNotExistError

""""
This module contains the three basic clases for Mars Rovers behavior and its
interaction with the environment (grid and obstacles). These classes could also be separeted
in differents files. For example: Grid in grid.py, Obstacles in obstacles.py and Rovers in rovers.py
"""

class Grid:
    """
    The Grid class will contain all the information of the plateau where Rovers can move. 
    This will be used to check if Rovers is inside the grid or not. 
    """
    def __init__(self, m:int, n:int) -> None:
        """
        This is the constructor of the class Grid. This class has the information of the custom
        grid (m X n) generated.

        :param m: This is the x dimension of the grid
        :type m: integer
        :param n: This is the y dimension of the grid.
        :type n: integer
        """
        self._m = m
        self._n = n

    def __getitem__(self, num:int) -> int:
        """
        This is the magic method to get an item given an index. In this case
        returns an element of the grid dimension tuple.

        :param num: this is the index
        :type num: integer
        :return: returns a number
        :rtype: integer
        """
        return (self._m, self._n)[num]

    def __contains__(self, indices:list) -> bool:
        """
        This magic method checks if a given point is found inside the grid.

        :param indices: list of x and y coordinates of the point
        :type indices: list
        :return: returns True if the point is inside the grid, else False
        :rtype: bool
        """
        return True if (indices[0] < self._m and indices[0] >= 0) and (indices[1] < self._n and indices[1] >= 0) else False

    @property
    def shape(self) -> tuple[int]:
        """
        This property method returns a tuple of the shape of the grid m X n

        :return: dimensions of the grid
        :rtype: tuple
        """
        return (self._m, self._n)

    def get_grid(self) -> np.array:
        """
        This function returns the grid as an object of numpy array

        :return: grid
        :rtype: numpy array object
        """
        return np.zeros((self._m, self._n))


class Rovers:
    """
    This is the Rovers class. This class contains all the information about the state and
    actions that Rovers can carry out. Rovers has two main states, the position where it can be 
    found in a certain moment and the direction it is pointing at. It has a method move that can receive
    either rotation instructions (L,R) or moving instructions (M). To determine the position and the direction
    it is facing we will use basic algebra on vectors mathematical objects. By applying matrix rotations we will obtain
    the direction where it points at. By adding the direction vector to the position vector we will obtain the next 
    position in the grid.
    """
    def __init__(self) -> None:
        """
        This is the constructor of the Rovers class. The state information of the Rovers 
        will be stored in this magic method. The default position of Rovers is at (0,0) and facing North ('N).
        First quadrant have been chosen for practicity.
        """
        self._pos: np.array = np.array((0,0))
        self._dir: str = 'N' #Default direction is facing North (N)
        self._dir_vec: np.array = np.array((0,1)) #Default direction vector is facing North (N)
        self._history: list[list[int]] = [self._pos.tolist()]  #history of positions
        self._can_move: bool = True

    def __str__(self) -> str:
        """
        This is the string magic method. It returns a string containing the
        current position of the Rovers.

        :return: current position of the rovers
        :rtype: string
        """
        if self._can_move: #If there is an obstacle we add an O
            return f'{self.position[0]}:{self.position[1]}:{self.direction}'
        else:
            return f'O:{self.position[0]}:{self.position[1]}:{self.direction}'

    @property
    def position(self) -> tuple[float]:
        """
        This property method returns the position of the rovers.

        :return: tuple of position coordinates
        :rtype: tuple
        """
        return self._pos
    
    @property
    def direction(self) -> str:
        """
        This is the property method of rovers direction. It returns N,S,W,E

        :return: direction where rovers is facing at current moment
        :rtype: string
        """
        return self._dir

    @property
    def vector(self) -> np.array:
        """
        This property method returns the direction pointer.
        (0,-1) --> points South (S)
        (0, 1) --> points North (N)
        (1, 0) --> points East (E)
        (-1, 0) --> points West (W)

        :return: Direction Vector (X,Y)
        :rtype: numpy array object
        """
        return self._dir_vec

    @property
    def history(self) -> list[list[int]]:
        """
        This property method returns the historical positions where Rovers
        has been during its exploration in Mars. This will be later used for
        drawing the path that it has followed.

        :return: list of positions
        :rtype: list
        """
        return self._history

    def can_move(self) -> bool:
        """
        This method is for knowing if rovers has found any obstacle and cannot move.

        :return: True if it can move, False if it cannot move anymore
        :rtype: bool
        """
        return self._can_move

    def ___wrap_around(self, pos:tuple, m:int, n:int):
        """
        When the Rovers reaches the final of the grid it wraps around it. It is like having periodic
        boundary conditions. This method allows the Rovers to wrap around the grid and continue its 
        exploration mission.

        :param pos: position of the Rovers.
        :type pos: tuple
        :param m: m length of the grid
        :type m: integer
        :param n: n lenght of the grid
        :type n: integer
        :return: returns the position after wrapping around the grid
        :rtype: tuple
        """
        pos_new = None
        if(pos[0]>m-1):
            pos_new = (pos[0]-m, pos[1])
        if(pos[0]<0):
            pos_new = (pos[0]+m, pos[1])
        if(pos[1]>n-1):
            pos_new = (pos[0], pos[1]-n)
        if(pos[1]<0):
            pos_new = (pos[0], pos[1]+n)
        else:
            pass
        return pos_new


    def __update_direction(self, vec:np.array) -> None:
        """
        This method updates the direction where the Rovers is facing. We use
        vector directions to know where it has to face. 

        :param vec: this is the vector direction after applying the rotation operation.
        :type vec: numpy array object.
        """
        if((vec == np.array((0,-1))).all()):
            self._dir = 'S'
        elif((vec == np.array((0, 1))).all()):
            self._dir = 'N'
        elif((vec == np.array((1, 0))).all()):
            self._dir = 'E'
        elif((vec == np.array((-1, 0))).all()):
            self._dir = 'W'
        else:
            raise DirectionNotFoundError(f'This direction vector {vec} does not exist')


    def move(self, command:str, grid:Grid, obstacles):
        """
        This is the move method of the Rovers. If the command is move ('M'). The robot
        checks if it can move or if there is any obstacle. If there is an obstacle the can_move
        object attribute is set to False and the Robot stays in the previous positions. However,
        if it can move it checks if the next position is in the grid or not. If the next position is not on the 
        MxN grid then it wraps around and obtains a positions that exists in the grid. Then. rovers move to the 
        next position. If the command is 'R' or 'L' means the robot has to rotate. If so, rotation operation
        on the direction vector is applied and the direction state (N,S,E,W) is updated. 

        :param command: This is the command: move or rotate. Posible options are M (move), R (rotate right), L (rotate left)
        :type command: string
        :param grid: This is the grid object of the grid created
        :type grid: Grid
        :param obstacles: This is an instance of the Obstacles class
        :type obstacles: Obstacles
        """
        if (command == 'M'):
            self._pos_new = self._pos + self._dir_vec
            if not obstacles.has(self._pos_new):
                #check if position is in grid 
                if(self._pos_new not in grid):
                    self._pos_new = self.___wrap_around(self._pos_new, grid.shape[0], grid.shape[1])
                self._pos = np.array((self._pos_new[0], self._pos_new[1]))
                self._history.append(self._pos.tolist())
            else:
                self._can_move = False
                print(f'Sorry captain, I have found an obstacle at position {self._pos_new}')
        #right rotation
        elif (command == 'R'):
            self._dir_vec = np.array((self._dir_vec[1], -self._dir_vec[0])) #rotation operation (90º clockwise)
            self.__update_direction(self._dir_vec)

        #left rotation
        elif (command == 'L'):
            self._dir_vec = np.array((-self._dir_vec[1], self._dir_vec[0])) #rotation operation (90º anti-clockwise)
            self.__update_direction(self._dir_vec)
        else:
            raise CommandDoesNotExistError(f'This command {command} does no exist. Choose one of these: M,R,L')



class Obstacles:
    """
    This class is the responsible for creating new obstacles inside the grid
    and checking if a certain vector position (X,Y) is found inside the grid.
    """
    def __init__(self) -> None:
        """
        This is the constructor of the class Obstacles. It has a list
        that will contain the positions of the random created obstacles.
        """
        self._obstacles = []

    def add_custom_obstacle(self, custom_obstacle_position:tuple[int]):
        """
        This function is for adding a custom obstacle position and not randomly. This
        method is mainly for later testing the rovers behavior against obstacles.

        :param custom_obstacle_position: This is a tuple of the position coordinates of the custom obstacle
        :type custom_obstacle_position: tuple of integers
        :returns: It returns the object
        :rtype: Obstacles instance
        """
        self._obstacles.append(custom_obstacle_position)
        return self

    def get_obstacles_positions(self) -> list[tuple[int]]:
        """
        This is the getter method for checking the list of obstacle positions.

        :return: Returns the list of tuples with position coordinates of the obstacles
        :rtype: List of tuples of integers (coordinates in the grid)
        """
        return self._obstacles

    def create_obstacles_in_grid(self, grid, num=1):
        """
        This method creates random (num) obstacles inside the grid.

        :param grid: This is the object created for the custom grid
        :type grid: Grid
        :param num: This is the number of obstacles created inside the grid
        :type num: integer
        :return: Returns the object instanciated
        :rtype: Obstacles
        """
        max_num_x = grid.shape[0]
        max_num_y = grid.shape[1]
        for i in range(num):
            random_obstacle = (random.randint(1,max_num_x-1), random.randint(0,max_num_y-1))
            if random_obstacle not in self._obstacles:
                self._obstacles.append(random_obstacle)
            #avoid that they are the same. Recursive
            else:
                self.create_obstacles_in_grid(grid, num=num-len(self._obstacles))
        return self
       
    def has(self, pos:np.array) -> bool:
        """
        This methodChecks if there is any obstacle in position pos
        Returns True if there is obstacle else false

        :param pos: this is the position where we want to know if there is an obstacle or not
        :type pos: numpy array object
        :return: Returns True if there is an obstacle in that position. Else returns False.
        :rtype: bool
        """
        return True if tuple(pos) in self._obstacles else False

