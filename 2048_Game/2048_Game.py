
#Clone of 2048 game.  Author : Thomson Kneeland  Python 2
#See: https://en.wikipedia.org/wiki/2048_(video_game)
#right/left/up/down keys act as user controls to manipulate numbers and consolidate pairs
# Uses Rice University GUI modules, will NOT run as standalone

import poc_2048_gui
import random

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
DOWNREV = 5

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1),
           DOWNREV: (1,0)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    line_sorted = []
 
    # create new list with numbered tiles at beginning, no zeros
    for dummy_num in range(len(line)):
        if line[dummy_num] != 0:
            line_sorted.append(line[dummy_num])
    
    # slide tiles and transform values
    if len(line_sorted) > 2:
        line_transform = []
        for num_dum in range(0, len(line_sorted)-1):
            if line_sorted[num_dum] == line_sorted[num_dum+1]:
                line_transform.append(line_sorted[num_dum] * 2)
                line_sorted.pop(num_dum)
                line_sorted.append(0)
            elif line_sorted[num_dum] != line_sorted[num_dum+1]: 
                line_transform.append(line_sorted[num_dum])          
        line_transform.append(line_sorted[-1])        
       
    # for sets of 2            
    elif len(line_sorted) == 2:
        line_transform = []
        if line_sorted[0] == line_sorted[1] != 0:
            line_transform.append(line_sorted[0]*2)
        else:
            line_transform = line_sorted
   
    # for sets of 1 or 0        
    else: 
        line_transform = line_sorted
 
    #append zeros to end of list       
    for dummy_num in range(len(line)-len(line_transform)):
        line_transform.append(0) 
    return line_transform

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = []
        down_rev_list = range(self.get_grid_width())
        down_rev_list.reverse()
        down_rev_list_trans = range(self.get_grid_height())
        down_rev_list_trans.reverse()
        
        # create dictionary for initial tile positions
        self._initial_tiles = {UP : [[0,number] for number in range(self.get_grid_width())],                                                                  
                            DOWN : [[self.get_grid_height() - 1, number] for number in range(self.get_grid_width())],
                            LEFT : [[number,0] for number in range(self.get_grid_height())],
                            RIGHT: [[number,self.get_grid_width()-1] for number in range(self.get_grid_height())],
                            DOWNREV : [[0, number] for number in down_rev_list]}
        # create dictionary for merge directions
        self._transform_tiles = {UP : [[0,number] for number in range(self.get_grid_height())],                                                                  
                            DOWN : [[self.get_grid_height() - 1, number] for number in range(self.get_grid_height())],
                            LEFT : [[number,0] for number in range(self.get_grid_height())],
                            RIGHT: [[number,self.get_grid_width()-1] for number in range(self.get_grid_height())],
                            DOWNREV : [[0, number] for number in down_rev_list_trans]}
        # create dictionary for merge ranges
        self._range = {UP : self._grid_height,
                      DOWN : self._grid_height,
                      LEFT : self._grid_width,
                      RIGHT : self._grid_width,
                      DOWNREV : self._grid_height}
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._grid_width)]for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()
  
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width
    
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        merge_list = []
        offset_grid = []
        grid_changed = False
        for cell in self._initial_tiles[direction]:
            for cross_cell in range(self._range[direction]):
                merge_list.append(self.get_tile(cell[0] + cross_cell * OFFSETS[direction][0],
                              cell[1] + cross_cell * OFFSETS[direction][1]))
                if len(merge_list) == len(range(self._range[direction])):
                    temp = merge(merge_list)

                    if temp != merge_list:
                        grid_changed = True 
                    offset_grid.append(merge(merge_list))
                    merge_list = []         
                    break
        #transform grid back to original orientation
        self._grid = offset_grid
        new_grid = []
        final_grid = []
        if direction == DOWN:
            direction = DOWNREV  
        for cell in self._transform_tiles[direction]:
            for cross_cell in range(self._grid_width):
                new_grid.append(self.get_tile(cell[0] + cross_cell * OFFSETS[direction][0],
                              cell[1] + cross_cell * OFFSETS[direction][1]))
                if len(new_grid) == len(range(self._grid_width)):
                        final_grid.append(new_grid)
                        new_grid = []
                        break  
        self._grid = final_grid
        if grid_changed:
            self.new_tile()
             
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #randomly select tile value 
        selection = random.random()
        if selection < .1:
            tile = 4
        else:
            tile = 2
            
        # create list of empty tiles  
        empty_tile_list = []
        for row in range(self._grid_height):
            for column in range(self._grid_width):
                if self._grid[row][column] == 0:
                    empty_tile_list.append([row,column])
        # if empty tile, enter value; if no empty tiles, print Game Over     
        if empty_tile_list == []:
            print "Grid Full, Make a Move!!"
        else:
            random_tile = random.choice(empty_tile_list)
            self.set_tile(random_tile[0],random_tile[1],tile)
 
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value       

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4,5))
