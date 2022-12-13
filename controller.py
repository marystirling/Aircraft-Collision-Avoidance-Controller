import math # needed for calculating the Euclidean distance between two aircrafts
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

##############################
## Bounds on the x, y, z axis
##############################
# bound values of the aircraft controller space for x, y, and z 
# 0 <= x, y, z <= 30
min_x = 0
max_x = 30
min_y = 0
max_y = 30
min_z = 0
max_z = 30

##############################
## Input Variables
##############################

# id of type string that is unique for each aircraft in the form plane_n, where n is an integer starting at 0 and incremented by 1 each new plane in vicinity
id = ""

# x, y, z coordinates of type int of the current location of the aircraft in question
current_x = 0
current_y = 0
current_z = 0

# target x and y coordiantes of type int for the landing location of the aircraft in question -> no z since all target destination will be on ground with z = 0
target_x = 0
target_y = 0

# TODO: add other positions of aircraft for input

# event(bool) type to indicate whether other aircraft are in the vicinity so we know whether we need to execute collision avoidance tasks
    # if other_aircraft = 0, then there are no other aircraft in the vicinity
    # if other_aircraft = 1, then there are 1 or more other aircraft in the vicinity
other_aircraft = 0


##############################
## State Variables
##############################

# direction of type int initiized to 0 degrees
# indicates the direction of flight in the xy-plane with possible values of 0, 90, 180, 270 degrees
direction = 0

# warning of type boolean to indicate whether another aircraft is in the warning cube dimensions of the aircraft in question
    # if warning = 0, then no warning 
    # if warning = 1, then warning meaning there is at least one aircraft in its vicinity at 2q boundary
warning = 0

# danger of type boolean to indicate whether another aircraft is in the danger cube dimensions of the aircraft in question
    # if danger = 0, then no danger
    # if danger = 1, then danger meaning there is at least one aircraft in its vicinity at 2d boundary
danger = 0

# collision of type boolean to indicate whether there has been a collision with this aircraft
    # if collision = 0, then no collision -> liveness properties ensures that this is always 0
    # if collision = 1, then collision -> another aircraft within 2d boundary   
collision = 0

# k of type int to indicate what clock cycle the controller is going through
# initialized as k = 0 since starting at the first clock cycle
k = 0

# start_k of type int to help ensure that only one move is made at each clock cycle
# initialized as start_k = 0 since starting at the first clock cycle
start_k = 0


##############################
## component logic
##############################
other_x, other_y, other_z = 0, 0, 0 
current_x, current_y, current_z = 0, 0, 0
target_x, target_y = 1, 1 
while True:
    
    print(f"current_x {current_x}, current_y {current_y}, current_z {current_z}")

    ##############################
    ## Task A 
    ##############################
    # this helps keep track that only one move of the aircraft is made each clock cycle 
    # will be used as a comparison at future tasks so that it only executes if no other move has been done
    # k will be incremented when the aircraft takes an action (whether turning or moving) 
    # future action tasks can only occur if k == start_k 
    start_k = k



    ##############################
    ## Task B
    ##############################
    # Given the current position, it generates the boundary of the warning zone which is a cube with edges of 2 km and the current aircraft at the center as (current_x, current_y, current_z)
    # Since each edge is 2 km, the warning zone is one coordinate space away from current aircraft or its vertices since 1 coordinate point moves 1 km at a time
    # Creates a list of the cube edge and vertices point called warning_cube
    warning_cube = []
    for z in  range(-1,2):
       for y in range(-1, 2):
            warning_cube.extend([
                (current_x - 1, current_y + y, current_z + z),
                (current_x, current_y + y, current_z + z),
                (current_x + 1, current_y + y, current_z + z),
            ])
    warning_cube.remove((current_x, current_y, current_z))


    ##############################
    ## Task C
    ##############################
    # See if another aircraft is in the warning zone of the current aircraft
    # if there is another aircraft and that aircraft is at the warning zone boundary, then changes warning to True so that future task can execute maneuver
    if other_aircraft and (other_x, other_y, other_z) in warning_cube:
        warning = True


    ##############################
    ## Task D
    ##############################
    # This task simulates taking off of the current aircraft if k = 0 (meaning it is the first clock cycle)
    # Can only take off if there is no other aircraft in the warning zone 
    # Takes off while in the 0 degrees direction so the x and z value of the current location will increment by 1
    # Increments start_k by 1 -> if other aircraft is in warning zone, this makes it wait for next clock cycle to still be k = 0 and wait for a clear takeoff
    if k == 0:
        current_x += 1
        current_z += 1
    