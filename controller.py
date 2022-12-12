


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
current_Y = 0
current_Z = 0

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
    # if collision = 1, then collision  
collision = 0

# k of type int to indicate what clock cycle the controller is going through
# initialized as k = 0 since starting at the first clock cycle
k = 0