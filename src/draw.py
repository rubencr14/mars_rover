import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
from config import NUMBER_OF_OBSTACLES, GRID_SIZE, DRAW_PATH
import warnings
#removing UserWarnings
warnings.filterwarnings("ignore")


def draw_rovers_path(rovers_positions:list, title:str, random_obstacles:list) -> None:
    """
    This method draws the path that the rovers followed during its exploration. It draws the path, the obstacles
    present in the grid and the wrap around (with blue line) if the mars rovers drops outside the grid. 

    :param rovers_positions: These are the vectors defining the positions that mars rovers has walked. 
    :type rovers_positions: list
    """

    _, ax = plt.subplots()
    min_val, max_val = 0, GRID_SIZE
    ind_array = np.arange(0, GRID_SIZE, 1.0)
    x, y = np.meshgrid(ind_array, ind_array)
    for _, (x_val, y_val) in enumerate(zip(x.flatten(), y.flatten())):
        ax.text(x_val, y_val, '', va='center', ha='center')

    #setting the x and y axis    
    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    ax.set_xticks(np.arange(max_val))
    ax.set_yticks(np.arange(max_val))

    #Creating black arrows for normal walking and blue arrows for wrapping around
    for elem in rovers_positions:
        dist = math.sqrt( (elem[1][0] - elem[0][0])**2 + (elem[1][1] - elem[0][1])**2 )
        if(dist >= max_val-1):
            ax.annotate("", elem[0], elem[1],label='arrow' , arrowprops={'arrowstyle':'<->', 'shrinkA': 0, 'shrinkB': 0, 'color' :'blue'})
        else:
            ax.annotate("", elem[0], elem[1], arrowprops={'arrowstyle':'<->', 'shrinkA': 0, 'shrinkB': 0})
    
    #plotting the obstacles given the random obstacles positions
    if(NUMBER_OF_OBSTACLES > 0):
        for random_obstacle in random_obstacles:
            x1 = random_obstacle[0]
            x2 = x1 + 1
            y2 = random_obstacle[1]
            y1 = y2 + 1
            ax.fill_between(x=[x1,x2], y1=[y1], y2=[y2], facecolor ='green')
    
    #Setting title, drawing grid, creating the legend and plotting
    ax.set_title(f'Final position: {title}')
    ax.grid()
    green_patch = mpatches.Patch(color='green', label='Obstacles')
    blue_patch = mpatches.Patch((0, 0), (1, 0), color='blue', label='Wrap around')
    black_patch = mpatches.Patch((0, 0), (1, 0), color='black', label='Rovers path')
    plt.legend(handles=[green_patch, blue_patch, black_patch])
    plt.show()