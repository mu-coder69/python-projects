'''
Natural selection simulator

NOT WORKING
'''

import pygame as pg
import numpy as np


pg.init()


##################### PREVIOUS PARAMETERS
height = 128
width = 128
wd = pg.display.set_mode((width, height))
clock = pg.time.Clock()
state = True
FPS = 100
white = (255, 255, 255)
####################

##################### CLASS CREATION
class particle:

    # # # # # # # # Not in use, future implementation
    inputs = ["WPX", "WPY"] ## genes WPX: World Position X, WPY: World Position Y
    internals = 3
    movements = ["RGT", "LFT"] ## genes RGT: Right, LFT: Left
    # # # # # # # # 

    def __init__(self):
        self.pos = np.random.randint(0, height, 2)
        self.color = np.random.randint(0, 200, 3)
        self.vel_x = np.random.randint(-5, 5)
        self.vel_y = np.random.randint(-5, 5)


        # # # # # # # # Not in use, future implementation
        self.inputs = np.random.choice(self.inputs, np.random.randint(1, 2))
        self.movements = np.random.choice(self.movements, np.random.randint(1, 2))
        # # # # # # # #
    
    def move(self, grid):
        ## move x
        new_pos = self.pos + (self.vel_x, 0)
        if new_pos[0] < 1:
            new_pos[0] = 1
        elif width -1 < new_pos[0]:
            new_pos[0] = width -1

        collision_status = self.check_collision(grid, self.pos, new_pos, "x")
        if not collision_status[0]:
            self.pos = new_pos
        else:
            self.pos[0] += collision_status[1]


        ## move y
        new_pos = self.pos + (0, self.vel_y)
        if new_pos[1] < 1:
            new_pos[1] = 1
        elif height -1 < new_pos[1]:
            new_pos[1] = height -1

        collision_status = self.check_collision(grid, self.pos, new_pos, "y")
        if not collision_status[0]:
            self.pos = new_pos
        else:
            self.pos[1] += collision_status[1]



    def check_collision(self, grid, prev_pos, new_pos, axis):

        if axis == "x":
            if new_pos[0] >= prev_pos[0]:
                status = grid[prev_pos[1], (prev_pos[0] +1):(new_pos[0] +1)]
            else:
                status = grid[prev_pos[1], (new_pos[0]):(prev_pos[0])]
            
            if status.size != 0 and sum(status) > 0:
                if new_pos[0] >= prev_pos[0]:
                    move = np.nonzero(status)[0][0]
                else:
                    move = -status.size + np.nonzero(status)[0][-1] +1

                return True, move
            else:
                return False, status.size
        else:
            if new_pos[1] >= prev_pos[1]:
                status = grid[(prev_pos[1] +1):(new_pos[1] +1), prev_pos[0]]
            else:
                status = grid[(new_pos[1]):(prev_pos[1]), prev_pos[0]]
            if status.size != 0 and sum(status) > 0:
                if new_pos[1] >= prev_pos[1]:
                    move = np.nonzero(status)[0][0]
                else:
                    move = -status.size + np.nonzero(status)[0][-1] +1
                
                return True, move
            else:
                return False, status.size
        


####################

#################### CODE PARAMETERS
n = 3000 # number of creatures
creatures = np.array([particle() for i in range(n)])
grid = np.zeros((height, width)) # world grid

####### Check duplicated places
c = 0
while c < creatures.shape[0]:
    prev = grid[tuple(creatures[c].pos)]
    if prev == 0:
        grid[tuple(creatures[c].pos)] += 1
    else:
        creatures = np.delete(creatures, c)
    c += 1
#######

print(f"not repeated creatures: {creatures.shape[0]}")
###################

# before = time.time()
while state:
    clock.tick(FPS)
    # now = time.time()
    # dt = now - before
    # before = now

    ################ Check to close the program
    for event in pg.event.get():
        if event.type == pg.QUIT:
            state = False
    ################

    wd.fill((255, 255, 255))

    grid = np.zeros((height, width), dtype=int)

    #################### SIMULATION
    for i in range(creatures.shape[0]):
        pg.draw.circle(wd, creatures[i].color, creatures[i].pos, radius=1)
        grid[(creatures[i].pos[1], creatures[i].pos[0])] = 1
    for i in range(creatures.shape[0]):
        creatures[i].move(grid)
    ####################

    pg.display.update()


pg.quit()

