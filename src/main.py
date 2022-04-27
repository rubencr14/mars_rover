import sys
from config import NUMBER_OF_OBSTACLES, GRID_SIZE, DRAW_PATH
from draw import draw_rovers_path
from mars import Grid, Rovers, Obstacles


def create_rovers_position(positions: list[int]) -> list[float]:
    """
    This function creates a list containing the position of the arrows according
    to rovers trajectory. It adds 0.5 so that the arrows are aligned in the center of the cell.

    :param positions: These are the positions where rovers has been
    :type positions: list of integers
    :return: arrows positions to plot
    :rtype: list of float numbers
    """
    final = []
    for index, position in enumerate(positions[1:]): #we do not want to take into account the first element
        arr = [(positions[index][0]+.5, positions[index][1]+.5), (position[0]+.5, position[1]+.5)] #0.5 to make the arrow be in center
        final.append(arr)
    return final

def main_rovers():
    """
    This is the main function of the rovers module. This method allows the user to enter the instructions
    in the terminal to tell the Mars Rovers to walk along the plateau (grid).
    """
    instructions = input('Write the instructions for rovers e.g MMRMMLM:  ')
    if(instructions == ''):
        sys.exit('Error: You have to enter the instructions so Mars Rovers can move!')
    grid = Grid(GRID_SIZE, GRID_SIZE)
    obstacles = Obstacles()
    random_obstacles = obstacles.create_obstacles_in_grid(grid, NUMBER_OF_OBSTACLES).get_obstacles_positions()
    rovers = Rovers()
    for instruction in instructions:
        if rovers.can_move():
            rovers.move(instruction, grid, obstacles)
        else:
            break
    positions_arr = create_rovers_position(rovers.history)
    if(DRAW_PATH):
        draw_rovers_path(positions_arr, rovers, random_obstacles)
    else:
        print('The final position is: ', rovers)

if __name__ == '__main__':
    main_rovers()