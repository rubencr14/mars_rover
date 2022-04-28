# Mars Rover Project
It is a programming project that solves the problem posed in https://katalyst.codurance.com/mars-rover

**FOR FULL DOCUMENTATION CHECK HTML FILES IN DOCS/BUILD/HTML. YOU CAN DOWNLOAD AND CLICK INDEX.HTML**

**AUTHOR: RUBÉN CAÑADAS RODRÍGUEZ**

**DATE: 27-04-2022**

**PYTHON VERSION: 3.10.0**

This is a basic documentation of rovers functionality. To be able to execute all the functions and make Mars Rovers walk and explore 
we must make sure we have all the required libraries installed:

```console
pip install -r requirements.txt
```
Once we have the libraries installed we can start. To move the rovers we only have to introduce in the terminal
the next command:

```console
python src/main.py
```
Then introduce the movements the Rovers has to do:

```console
Write the instructions for rovers e.g MMRMMLM:
```
When you introduce the movements, Mars Rovers will perform them and a plot of its path will appear.

We can change some parameters in the config.py file inside the src directory. For example, we can 
set the number of obstacles in the grid, the size of the grid and also if we want to create the draw
of the rovers path.

Inside the src directory we find the tests directory. This are basic integration tests to check
the proper behavior of the Rovers in the grid. Unit tests for checking the functionality of each method could also be done 
in future work. If pytest is installed we only have to run the next command:

```console
python pytest

   ============================= test session starts ==============================
   platform darwin -- Python 3.10.0, pytest-7.1.2, pluggy-1.0.0
   rootdir: /Users/rubencr/Desktop/rovers
   plugins: Faker-13.3.4
   collected 10 items                                                             

   src/tests/test_rovers.py ..........                                      [100%]

   ============================== 11 passed in 1.70s ==============================
```
This means that the tests have passed properly without any failure. We also can control rovers movement from python
importing the corresponding modules as follows:


```python
from mars import Grid, Rovers, Obstacles
   from config import NUMBER_OF_OBSTACLES, GRID_SIZE

   instructions = 'MMRMMLM'
   grid = Grid(GRID_SIZE, GRID_SIZE)
   obstacles = Obstacles()
   random_obstacles = obstacles.create_obstacles_in_grid(grid, NUMBER_OF_OBSTACLES).get_obstacles_positions()
   rovers = Rovers()
   for instruction in instructions:
      if rovers.can_move():
         rovers.move(instruction, grid, obstacles)
      else:
         break
```
For more information you can check docs/build/html files for full documentation.
