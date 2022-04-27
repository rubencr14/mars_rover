import pytest
from mars import Rovers, Grid, Obstacles
from config import GRID_SIZE

############################################################
#                                                          #
#         HELPER FUNCTIONS FOR TESTING                     #
#                                                          #
############################################################

def rotation(instructions, result):
    """
    Given the instructions and the expected result this function
    asserts that the computed result by rotation corresponds
    to the expected one.

    :param instructions: A list of characters containing instructions for the robot
    :type instructions: string
    :param result: This is a character of the orientation of the rovers
    :type result: string
    """
    grid = Grid(GRID_SIZE, GRID_SIZE)
    rovers = Rovers()
    obstacles = Obstacles()
    for char in instructions:
        rovers.move(char, grid, obstacles)
    assert rovers.direction == result

def moves(instructions, position):
    """
    Given the instructions and the expected result this function
    asserts that the computed result by movement corresponds
    to the expected one.

    :param instructions: A list of characters containing instructions for the robot
    :type instructions: string
    :param position: String containing the position. e.g. 2:3:N
    :type postion: string
    """
    grid = Grid(GRID_SIZE, GRID_SIZE)
    rovers = Rovers()
    obstacles = Obstacles()
    for char in instructions:
        rovers.move(char, grid, obstacles)
    assert str(rovers) == position

def move_to_obstacles(instructions):
    """
    This function is for creating an obstacle in a specific position to 
    later test if mars rovers stops when there is an obstacle in front.

    :param instructions: A list of characters containing instructions for the robot
    :type instructions: string
    """
    grid = Grid(GRID_SIZE, GRID_SIZE)
    rovers = Rovers()
    obstacles = Obstacles().add_custom_obstacle((2,5))
    for char in instructions:
        rovers.move(char, grid, obstacles)
    assert (rovers.position == (2,4)).all()



#############################################################
#                                                           #
#         TESTS FUNCTIONS FOR TESTING WITH PYTEST           #
#                                                           #
#############################################################

def test_right_rotation_east():
    """
    This test assures that after rotation to the right,
    starting from (0,0,N), it faces East (E).
    """
    rotation('R', 'E')

def test_right_rotation_south():
    """
    This test assures that after two rotations to the right,
    starting from (0,0,N), it faces South (S).
    """
    rotation('RR', 'S')

def test_right_rotation_west():
    """
    This test assures that after three rotations to the right,
    starting from (0,0,N), it faces West (W).
    """
    rotation('RRR', 'W')

def test_right_rotation_north():
    """
    This test assures that after four rotations to the right,
    starting from (0,0,N), it faces North (N).
    """
    rotation('RRRR', 'N')

def test_left_rotation_east():
    """
    This test assures that after one rotation to the left,
    starting from (0,0,N), it faces West (W).
    """
    rotation('L', 'W')

def test_left_rotation_south():
    """
    This test assures that after two rotations to the left,
    starting from (0,0,N), it faces South (S).
    """
    rotation('LL', 'S')

def test_left_rotation_west():
    """
    This test assures that after three rotations to the left,
    starting from (0,0,N), it faces East (E).
    """
    rotation('LLL', 'E')

def test_left_rotation_north():
    """
    This test assures that after four rotations to the left,
    starting from (0,0,N), it faces North (N).
    """
    rotation('LLLL', 'N')

def test_move():
    """
    This test assures the combination of movements and rotations.
    """
    moves('MMRMMLM', '2:3:N')

def test_move_with_wrap_around():
    """
    This test checks if the wrap around works properly
    given instructions that force the mars rovers to go
    outside the grid.
    """
    moves('MMRMMMLMRMRMMMMM', '4:8:S')

def test_stop_if_obstacle():
    """
    This test checks if the mars rovers stops when it finds an obstacle
    in the next cell.
    """
    move_to_obstacles('MMRMMLMMMM')