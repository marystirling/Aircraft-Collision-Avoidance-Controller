import time 
import random # used to initialize the iniitial and target destinations of the aircraft

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
    # if other_aircraft = False, then there are no other aircraft in the vicinity
    # if other_aircraft = True, then there are 1 or more other aircraft in the vicinity
other_aircraft = False


##############################
## State Variables
##############################

# direction of type int initiized to 0 degrees
# indicates the direction of flight in the xy-plane with possible values of 0, 90, 180, 270 degrees
direction = 0

# warning of type boolean to indicate whether another aircraft is in the warning cube dimensions of the aircraft in question
    # if warning = False, then no warning 
    # if warning = True, then warning meaning there is at least one aircraft in its vicinity at 2q boundary
warning = False

# danger of type boolean to indicate whether another aircraft is in the danger cube dimensions of the aircraft in question
    # if danger = False, then no danger
    # if danger = True, then danger meaning there is at least one aircraft in its vicinity at 2d boundary
danger = False

# collision of type boolean to indicate whether there has been a collision with this aircraft
    # if collision = False, then no collision -> liveness properties ensures that this is always 0
    # if collision = True, then collision -> another aircraft within 2d boundary   
collision = False

# k of type int to indicate what clock cycle the controller is going through
# initialized as k = 0 since starting at the first clock cycle
k = 0

# start_k of type int to help ensure that only one move is made at each clock cycle
# initialized as start_k = 0 since starting at the first clock cycle
start_k = 0

# landing of type string tells which value will be decremented while landing (x or y)
# the process of landing the aircraft decrements both the z-value and the x or y values so we want to be sure that there is enough distance from one to land successfully
# if landing = x, then landing will occur in either the 0 or 180 degree direction
# if landing = y, then landing will occur in either the 90 or 270 degree direction
# landing is initialized to none since we do not the distances from the current location to the targest destination for both the x's and y's
landing = None


# reached of type boolean to indicate whether or not hte aircraft has reached its targest destination or not
# initialized as reached = False since aircraft starts in a different location than its targest destination
# when reached = True, aircraft controller will stop as the aircraft would have landed
reached = False


##############################
## Initial and Target Positions
##############################
# This randomizes the initial and target x and y values between the values of  0 and 30 (bounds) 
current_x, current_y, target_x, target_y = random.randint(0, 30), random.randint(0, 30), random.randint(0, 30), random.randint(0, 30)
current_z = 0
print(f"curr_x {current_x}, target_x {target_x}, current_y {current_y}, target_y {target_y}")
# Assumption that the takeoff and landing destinations must be at least 1 km apart since the initial position != target position
# This loop ensures that this assumption remains true without having to manually set values each simulation
while abs(current_x - target_x) < 1 or abs(current_y - target_y) < 1:
    print(f"curr_x {current_x}, target_x {target_x}, current_y {current_y}, target_y {target_y}")
    if abs(current_x - target_x) < 1:
        target_x = random.randint(0, 30)
    if abs(current_y - target_y) < 1:
        target_y = random.randint(0, 30)

#current_x, current_y, current_z = 1, 0, 2
#current_x, current_y, current_z = 0, 0, 0
other_x, other_y, other_z = 1, 0, 1
other_aircraft = True

while not reached:
    print("\nNEW CLOCK CYCLE")
    print(f"current_x {current_x}, current_y {current_y}, current_z {current_z}")
    print(f"target_x {target_x}, target_y {target_y}, target_z 0")
    print(f"direction is {direction}")
    print(f"distance of x's is {abs(current_x - target_x)}")
    print(f"distance of y's is {abs(current_y - target_y)}")
    print(f"landing is {landing}")
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
    print(warning_cube)
    print(f"other (x, y, z) is ({other_x}, {other_y}, {other_z})")
    ##############################
    ## Task C
    ##############################
    # See if another aircraft is in the warning zone of the current aircraft
    # if there is another aircraft and that aircraft is at the warning zone boundary, then changes warning to True so that future task can execute maneuver
    # It also keeps track of the (x,y,z) coordinates of those aircraft in the list warning_coordinates
    # warning_coordinates resets back to empty list each clock cycle to remove any coordinate points not in warning zone anymore
    warning_coordinates = []
    if other_aircraft and (other_x, other_y, other_z) in warning_cube:
        warning = True
        warning_coordinates.append((other_x, other_y, other_z))
    else:
        warning = False
    print(f"warning is {warning}")
    #warning_coordinates.append((2, 0, 3))
    #warning_coordinates.append((2, 0, 1))
    #warning_coordinates.append((2, 0, 2))
    print(f"warning coordinates is {warning_coordinates}")
    

    ##############################
    ## Task D
    ##############################
    # This task simulates a potential collision avoidance maneuver if there is another aircraft and a warning. 
    # It looks at the coordinates in warning_coordinates
    # Collision maneuvers will only occur if there is a plane on the same z-valued altitude in warning_coordinates
    # If there is some aircraft in the same z-valued altitude as the current aircraft than it will change warning_break_flag to false to signal a maneuver action is necessary
    if warning:
        # If warning_break_flag stays True, then there is no other aircraft in the warning zone on the same z-altitude, so resume normal operations
        warning_break_flag = True
        for point in warning_coordinates:
            if point[2] == current_z:
                warning_break_flag = False
                # If this is changed to False, then need to perform some collision maneuver
                # Else, the aircraft will resume to normal actions 
        if not warning_break_flag: 
        #First, check direction plane is in, then perform the necessary maneuver in order of this precedence: 
            # 1. If the altitude is greater than 1 and the location to descend one space is free, then do so. Or, if the next descent is the target location, then land
            # 2. If the next space forward in direction flying is free on same z-value, then move forward by one coordinate space in x or y direction (depends on direction)
            # 3. If the coordinate space for the aircraft to ascend by one coordinate space is available, then fly aircraft in upward direction
            # 4. If all of these spaces are in warning_coordinates for the current direction, then change direction by a factor of 90
            if direction == 0:
                if ((current_x + 1, current_y, current_z - 1) not in warning_coordinates and current_z > 1) or (current_x + 1, current_y, current_z - 1) == (target_x, target_y, 0):
                    current_x += 1
                    current_z -= 1
                elif  (current_x + 1, current_y, current_z) not in warning_coordinates:
                    current_x += 1
                elif (current_x + 1, current_y, current_z + 1) not in warning_coordinates:
                    current_x += 1
                    current_z += 1
                else:
                    direction = 90
            elif direction == 90:
                if ((current_x, current_y + 1, current_z - 1) not in warning_coordinates and current_z > 1) or (current_x, current_y + 1, current_z - 1) == (target_x, target_y, 0):
                    current_y += 1
                    current_z -= 1
                elif (current_x, current_y + 1, current_z) not in warning_coordinates:
                    current_y += 1
                elif (current_x, current_y + 1, current_z + 1) not in warning_coordinates:
                    current_y += 1
                    current_z += 1
                else:
                    direction = 0
            elif direction == 180:
                if ((current_x - 1, current_y, current_z - 1) not in warning_coordinates and current_z > 1) or (current_x - 1, current_y, current_z - 1) == (target_x, target_y, 0):
                    current_x -= 1
                    current_z -= 1
                elif (current_x - 1, current_y, current_z) not in warning_coordinates:
                    current_x -= 1
                elif (current_x - 1, current_y, current_z + 1) not in warning_coordinates:
                    current_x -= 1
                    current_z += 1
                else:
                    direction = 90
            elif direction == 270:               
                if ((current_x, current_y - 1, current_z -  1) not in warning_coordinates and current_z > 1) or (current_x, current_y - 1, current_z - 1) == (target_x, target_y, 0):
                    current_y -= 1
                    current_z -= 1
                elif (current_x, current_y - 1, current_z) not in warning_coordinates:
                    current_y -= 1
                elif (current_x, current_y - 1, current_z + 1) not in warning_coordinates:
                    current_y -= 1
                    current_z += 1
                else:
                    direction = 0 
            # increment k by 1 to indicate that an action has been performed by the aircraft during this clock cycle
            k += 1



    ##############################
    ## Task E
    ##############################
    # This task simulates taking off of the current aircraft if k = 0 (meaning it is the first clock cycle)
    # Can only take off if there is no other aircraft in the warning zone 
    # Takes off while in the 0 degrees direction so the x and z value of the current location will increment by 1
    # If warning = True, then increment start_k to prevnt future moves this clock cycle and start_k will be reset at next clock cycle
    # If warning = False, then increment k to indicate that a move has been made at this clock cycle 
    if k == 0:
        if not warning:
            current_x += 1
            current_z += 1
            k = 1
        elif warning:
            start_k += 1
            print("is this where it is stopping")


    ##############################
    ## Task F
    ##############################
    # This task focuses on the descent of the aircraft to its targest destination.
    # Depending on the direction of the aircraft, descent decrements the z-value and either the x or y value of the aircraft
    # Descent is ideal if the length from either the x or y distance from the current location to the targest destination equals the altitude (z-value)
    if abs(current_x - target_x) <= abs(current_y - target_y):
        # According to this clock cycle, the aircraft will be landing in either the 90 or 270 degree direction since there is more distance to descent in the y-direction
        landing = "y"
    elif abs(current_y - target_y) < abs(current_x - target_x):
        # According to this clock cycle, the aircraft will be landing in either the 0 or 180 degree direction since there is more distance to descent in the x-direction
        landing = "x"

    ##############################
    ## Task G
    ##############################
    # This task ensures that there is enough space to land in the x and y direction
    # If landing = "x", and the altiitude z is greater than distance of the x-value from its target destination, then there is not enough room to land (same if landing = "Y" with y values)
    if start_k == k and ((landing == "x" and current_z > abs(current_x - target_x)) or (landing == "y" and current_z > abs(current_y - target_y))):
        if landing == "x":
            # If landing in x-directions (0 or 180) then we need to move or rotate in one of those directions to give aircraft more space to land
            if direction == 0:
                current_x += 1
            elif direction == 90:
                direction = 0
            elif direction == 180:
                current_x -= 1
            elif direction == 270:
                direction = 0
        elif landing == "y":
            # If landing in y-directions (90 or 270) then we need to move or rotate in one of those directions to give aircraft more space to land
            if direction == 0:
                direction = 90
            elif direction == 90:
                current_y += 1
            elif direction == 180:
                direction = 90
            elif direction == 270:
                current_y -= 1
        # increment k by 1 to indicate that an action has been performed by the aircraft during this clock cycle
        k += 1



    ##############################
    ## Task H
    ##############################
    # First, we want to prioritize the x and y values of the current location first
    # We first check which x or y distance is less than the distance from the target location and prioritize that direction first
    # Only perform an action if start_k == k, meaning that no action has been taken yet in this clock cycle
    if start_k == k and (abs(current_x - target_x) < abs(current_y - target_y) or current_y == target_y) and  current_x != target_x and current_z != 0: 
        # Distance of the x's is less than the distance of the y's so we will prioritize the x position of the aircraft first given that the current_x is not already at target x and z is not 0
        # This code now either changes the direction of flight or moves the aircraft in the positive or negative x-direction or begins descent if landing = "x" and conditions ready
        if landing == "x" and abs(current_x - target_x) == current_z and current_y == target_y:
            # landing state variable is in 0 or 180 direction and the descent distance is ideal since both x and z change values for descent, and the y-value is the same as the targest destination
            # If needed, adjust the direction of flight or changing the x-value as needed to get 0 or 180 degrees
            # If correct direction, then change x-value and decrement z-value
            if current_x < target_x:
                # since the current_x is less than the target_x, we need to be in 0 degrees direction, so we either adjust direction angle by factor of 90 or if 0, then increment current_x
                if direction == 0:
                    current_x += 1
                    current_z -= 1
                elif direction == 90:
                    direction = 0
                elif direction == 180:
                    direction = 90
                elif direction == 270:
                    direction = 0
            elif current_x > target_x:
                # since the current_x is greater than the target_x, we need to be in 180 degrees direction, so we either adjust direction angle by factor of 90 or if 180, then decrement current_x
                if direction == 0:
                    direction = 90
                elif direction == 90:
                    direction = 180
                elif direction == 180:
                    current_x -= 1
                    current_z -= 1
                elif direction == 270:
                    direction == 180
            

        elif current_x < target_x:
            # if the current x position of the aircraft is less than the target x, then the aircraft should be in the 0 degrees direction
            # if the direction of flight is not already at 0 degrees, then change the direction by a factor of 90 degrees in order to be at 0 degrees or closer to it
            # if the direction of flight was already at 0 degrees from the previous clock cycle, then move the aircraft in the x-direction by incrementing current_x by 1
            if direction == 0:
                current_x += 1
            elif direction == 90:
                direction = 0
            elif direction == 180:
                direction = 90
            elif direction == 270:
                direction = 0
        elif current_x > target_x:
            # if the current x position of the aircraft is greater than the target x, then the aircraft should be in the 180 degrees direction
            # if the direction of flight is not already at 180 degrees, then change the direction by a factor of 90 degrees in order to be at 180 degrees or closer to it
            # if the direction of flight was already at 180 degrees from the previous clock cycle, then move the aircraft in the x-direction by decrementing current_x by 1
            if direction == 0:
                direction = 90
            elif direction == 90:
                direction = 180
            elif direction == 180:
                current_x -= 1
            elif direction == 270:
                direction = 180
           
        # increment k by 1 to indicate that an action has been performed by the aircraft during this clock cycle
        k += 1

    elif start_k == k and (abs(current_y - target_y) < abs(current_x - target_x) or current_x == target_x) and current_y != target_y and current_z != 0: 
        # Distance of the y's is less than the distance of the x's so now we prioritize the the y position of the aircraft given that the current_y is not already at target y and z is not 0
        # This code now either changes the direction of flight or moves the aircraft in the positive or negative y-direction
        if landing == "y" and abs(current_y - target_y) == current_y and current_x == target_x:
            # landing state variable is in 90 or 270 direction and the descent distance is ideal since both y and z change values for descent, and the x-value is the same as the targest destination
            # If needed, adjust the direction of flight or changing the x-value as needed to get 90 or 270 degrees
            # If correct direction, then change x-value and decrement z-value
            if current_y < target_y:
                # since the current_y is less than the target_y, we need to be in 90 degrees direction, so we either adjust direction angle by factor of 90 or if 90, then increment current_y
                if direction == 0:
                    direction = 90
                elif direction == 90:
                    current_y += 1
                    current_z -= 1
                elif direction == 180:
                    direction = 90
                elif direction == 270:
                    direction = 0
            elif current_y > target_y:
                # since the current_y is greater than the target_y, we need to be in 270 degrees direction, so we either adjust direction angle by factor of 90 or if 270, then decrement current_y
                if direction == 0:
                    direction = 270
                elif direction == 90:
                    direction = 0
                elif direction == 180:
                    direction = 270
                elif direction == 270:
                    current_y -= 1
                    current_z -= 1
        elif current_y < target_y:
            # if the current y position of the aircraft is less than the target y, then the aircraft should be in the 90 degrees direction
            # if the direction of flight is not already at 90 degrees, then change the direction by a factor of 90 degrees in order to be at 90 degrees or closer to it
            # if the direction of flight was already at 90 degrees from the previous clock cycle, then move the aircraft in the y-direction by incrementing current_x by 1
            if direction == 0:
                direction = 90
            elif direction == 90:
                current_y += 1
            elif direction == 180:
                direction = 90
            elif direction == 270:
                direction = 0
        elif current_y > target_y:
            # if the current y position of the aircraft is greater than the target y, then the aircraft should be in the 270 degrees direction
            # if the direction of flight is not already at 270 degrees, then change the direction by a factor of 90 degrees in order to be at 270 degrees or closer to it
            # if the direction of flight was already at 270 degrees from the previous clock cycle, then move the aircraft in the y-direction by decrementing current_y by 1
            if direction == 0:
                direction = 270
            elif direction == 90:
                direction = 0
            elif direction == 180:
                direction = 270
            elif direction == 270:
                current_y -= 1
        # increment k by 1 to indicate that an action has been performed by the aircraft during this clock cycle
        k += 1



    time.sleep(2)


    ##############################
    ## Task I
    ##############################
    # Task that outputs the current x, y, and z values of the current aircraft
    # all output of type int 
    out_x = current_x
    out_y = current_y
    out_z = current_z

    ##############################
    ## Task J
    ##############################
    # check whether the output (x, y, z) is equal to the target destination values
    # if output (x, y, z) = target (x, y, 0), then state variable reached = True which breaks out of the loop (simulating the turning off of this aircraft controller)
    if out_x == target_x and out_y == target_y and out_z == 0:
        reached = True