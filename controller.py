import time 

class Controller:

    ##############################
    ## Initialize State Variables
    ##############################
    def __init__(self):


        # direction of type int initiized to 0 degrees
        # indicates the direction of flight in the xy-plane with possible values of 0, 90, 180, 270 degrees
        self.direction = 0

        # warning of type boolean to indicate whether another aircraft is in the warning cube dimensions of the aircraft in question
            # if warning = False, then no warning 
            # if warning = True, then warning meaning there is at least one aircraft in its vicinity at 2d boundary
        self.warning = False


        # collision of type boolean to indicate whether there has been a collision with this aircraft
            # if collision = False, then no collision -> liveness properties ensures that this is always 0
            # if collision = True, then collision -> another aircraft within 2d boundary  
        # Algorithm ensures that this will never change to True -> only used as a safety monitor and for testing purposes 
        self.collision = False

        # k of type int to indicate what clock cycle the controller is going through
        # initialized as k = 0 since starting at the first clock cycle
        self.k = 0

        # start_k of type int to help ensure that only one move is made at each clock cycle
        # initialized as start_k = 0 since starting at the first clock cycle
        self.start_k = 0

        # landing of type string tells which value will be decremented while landing (x or y)
        # the process of landing the aircraft decrements both the z-value and the x or y values so we want to be sure that there is enough distance from one to land successfully
        # if landing = x, then landing will occur in either the 0 or 180 degree direction
        # if landing = y, then landing will occur in either the 90 or 270 degree direction
        # landing is initialized to none since we do not the distances from the current location to the targest destination for both the x's and y's
        self.landing = None


        # reached of type boolean to indicate whether or not the aircraft has reached its targest destination or not
        # initialized as reached = False since aircraft starts in a different location than its targest destination
        # when reached = True, aircraft controller will stop as the aircraft would have landed
        self.reached = False

        # warning_cube is a list of tuple (x, y, z) coordinates to indiciate the coordinates around the current aircraft that are potential warning points
        # initialized as an empty list, but reset every clock cycle to collect the (x,y,z) points that are on the warning zone boundary of the current aircraft
        # used to compare to other aircraft coordinates to see if there is a match in order to perform a collision avoidance maneuver
        self.warning_cube = []

        # warning_coordinates is a list of tuple (x, y, z) coordinates to indicate if another aircraft is in the warning zone of the current aircraft
        # initialized as an empty list, but reset every clock cycle to collect the (x,y,z) points if another aircraft matches a coordinate in warning_cube
        # if the list is nonempty at a clock cycle, then a collision avoidance maneuver is needed
        self.warning_coordinates = []


    #############################
    ## CONTROLLER COMPONENT
    #############################
    def ClockCycle(self, current_x, current_y, current_z, target_x, target_y, other_aircraft):

        ##############################
        ## Task A 
        ##############################
        # this helps keep track that only one move of the aircraft is made each clock cycle 
        # will be used as a comparison at future tasks so that it only executes if no other move has been done
        # k will be incremented when the aircraft takes an action (whether turning or moving) 
        # future action tasks can only occur if k == start_k 
        self.start_k = self.k



        ##############################
        ## Task B
        ##############################
        # Given the current position, it generates the boundary of the warning zone which is a cube with edges of 2 km and the current aircraft at the center as (current_x, current_y, current_z)
        # Since each edge is 2 km, the warning zone is one coordinate space away from current aircraft or its vertices since 1 coordinate point moves 1 km at a time
        # Creates a list of the cube edge and vertices point called warning_cube
        self.warning_cube = []
        for z in  range(-1,2):
                for y in range(-1, 2):
                    self.warning_cube.extend([
                        (current_x - 1, current_y + y, current_z + z),
                        (current_x, current_y + y, current_z + z),
                        (current_x + 1, current_y + y, current_z + z),
                    ])
        self.warning_cube.remove((current_x, current_y, current_z))
        

        
        ##############################
        ## Task C
        ##############################
        # This reports that a collision has occured
        # Collision occurs if aircraft goes within the warning zone, so if the current aircraft coordinates equal another 
        # This is used as a safety monitor and testing purposes
        # Algorithm and liveness properties ensures that this will never execute
        for coordinate in other_aircraft.values():
            # OUR SYSTEM ENSURES THAT THERE ARE NO COLLISIONS SO THIS SHOULD NEVER BE TRUE
            if coordinate == (current_x, current_y, current_z):
                print("COLLISION")
                self.collision = True
                if self.collision:
                    exit()


        ##############################
        ## Task D
        ##############################
        # See if another aircraft is in the warning zone of the current aircraft
        # if there is another aircraft and that aircraft is at the warning zone boundary, then changes warning to True so that future task can execute collision avoidance maneuver
        # It also keeps track of the (x,y,z) coordinates of those aircraft in the list warning_coordinates
        # warning_coordinates resets back to empty list each clock cycle to remove any coordinate points not in warning zone anymore
        self.warning_coordinates = []
        self.warning = False
        for coordinate in other_aircraft.values():
            if coordinate in self.warning_cube:
                self.warning = True
                self.warning_coordinates.append(coordinate)

 
        ##############################
        ## Task E
        ##############################
        # This task simulates a potential collision avoidance maneuver if there is another aircraft and a warning. 
        # It looks at the coordinates in warning_coordinates
        # Collision maneuvers will only occur if there is a plane on the same z-valued altitude in warning_coordinates
        # To see if there is one, we change warning back to False and only change it back to True if z-values match the current aircraft's coordinate
        if self.warning:
            # If self.warning stays False, then there is no other aircraft in the warning zone on the same z-altitude, so resume normal operations
            self.warning = False
            for point in self.warning_coordinates:
                if point[2] == current_z:
                    self.warning = True
                    # If this is changed vback to True, then need to perform some collision maneuver
                    # Else, the aircraft will resume to normal actions 
            if self.warning: 
            #First, check direction plane is in, then perform the necessary maneuver in order of this precedence: 
                # 1. If the next descent is the target location, then land the aircraft
                # 2. If the coordinate space for the aircraft to ascend by one coordinate space is available, then fly aircraft in upward direction
                # 3. If the next space forward in direction flying is free on same z-value, then move forward by one coordinate space in x or y direction (depends on direction)
                # 4. If all of these spaces are in warning_coordinates for the current direction, then change direction by a factor of 90
                if self.direction == 0:
                    if (current_x + 1, current_y, current_z - 1) == (target_x, target_y, 0):
                        current_x += 1
                        current_z -= 1
                    elif (current_x + 1, current_y, current_z + 1) not in self.warning_coordinates:
                        current_x += 1
                        current_z += 1
                    elif  (current_x + 1, current_y, current_z) not in self.warning_coordinates:
                        current_x += 1
                    else:
                        self.direction = 90
                elif self.direction == 90:
                    if (current_x, current_y + 1, current_z - 1) == (target_x, target_y, 0):
                        current_y += 1
                        current_z -= 1
                    elif (current_x, current_y + 1, current_z + 1) not in self.warning_coordinates:
                        current_y += 1
                        current_z += 1
                    elif (current_x, current_y + 1, current_z) not in self.warning_coordinates:
                        current_y += 1
                    else:
                        self.direction = 0
                elif self.direction == 180:
                    if  (current_x - 1, current_y, current_z - 1) == (target_x, target_y, 0):
                        current_x -= 1
                        current_z -= 1
                    elif (current_x - 1, current_y, current_z + 1) not in self.warning_coordinates:
                        current_x -= 1
                        current_z += 1
                    elif (current_x - 1, current_y, current_z) not in self.warning_coordinates:
                        current_x -= 1
                    else:
                        self.direction = 90
                elif self.direction == 270:               
                    if  (current_x, current_y - 1, current_z - 1) == (target_x, target_y, 0):
                        current_y -= 1
                        current_z -= 1
                    elif (current_x, current_y - 1, current_z + 1) not in self.warning_coordinates:
                        current_y -= 1
                        current_z += 1
                    elif (current_x, current_y - 1, current_z) not in self.warning_coordinates:
                        current_y -= 1
                    else:
                        self.direction = 0 
                # increment k by 1 to indicate that an action has been performed by the aircraft during this clock cycle
                self.k += 1



        ##############################
        ## Task F
        ##############################
        # This task simulates taking off of the current aircraft if k = 0 (meaning it is the first clock cycle)
        # Can only take off if there is no other aircraft in the upward space the current aircraft will occupy
        # Takes off while in the 0 degrees self.direction so the x and z value of the current location will increment by 1
        # If takeoff clear, then increment start_k to prevnt future moves this clock cycle and start_k will be reset at next clock cycle
        # If takeoff not clear, then increment k to indicate that a move has been made at this clock cycle 
        if self.k == 0:
            if (current_x + 1, current_y, current_z + 1) not in self.warning_coordinates:
                current_x += 1
                current_z += 1
                self.k = 1
            else:
                self.start_k += 1



        ##############################
        ## Task G
        ##############################
        # This task focuses on the descent of the aircraft to its targest destination.
        # Depending on the direction of the aircraft, descent decrements the z-value and either the x or y value of the aircraft
        # Descent is ideal if the length from either the x or y distance from the current location to the targest destination equals the altitude (z-value)
        if abs(current_x - target_x) <= abs(current_y - target_y):
            # According to this clock cycle, the aircraft will be landing in either the 90 or 270 degree direction since there is more distance to descend in the y-direction
            self.landing = "y"
        elif abs(current_y - target_y) < abs(current_x - target_x):
            # According to this clock cycle, the aircraft will be landing in either the 0 or 180 degree direction since there is more distance to descend in the x-direction
            self.landing = "x"

        ##############################
        ## Task H
        ##############################
        # This task ensures that there is enough space to land in the x and y direction
        # If landing = "x", and the altiitude z is greater than distance of the x-value from its target destination, then there is not enough room to land (same if landing = "Y" with y values)
        if self.start_k == self.k and ((self.landing == "x" and current_z > abs(current_x - target_x)) or (self.landing == "y" and current_z > abs(current_y - target_y))):
            if self.landing == "x":
                # If landing in x-directions (0 or 180) then we need to move or rotate in one of those directions to give aircraft more space to land
                if self.direction == 0:
                    current_x += 1
                elif self.direction == 90:
                    self.direction = 0
                elif self.direction == 180:
                    current_x -= 1
                elif self.direction == 270:
                    self.direction = 0
            elif self.landing == "y":
                # If landing in y-directions (90 or 270) then we need to move or rotate in one of those directions to give aircraft more space to land
                if self.direction == 0:
                    self.direction = 90
                elif self.direction == 90:
                    current_y += 1
                elif self.direction == 180:
                    self.direction = 90
                elif self.direction == 270:
                    current_y -= 1
            # increment k by 1 to indicate that an action has been performed by the aircraft during this clock cycle
            self.k += 1



        ##############################
        ## Task I
        ##############################
        # This task calculates the next move of the aircraft if no previous move has been made (collision avoidance, landing to target, takeoff)
        # We first check which x or y distance is less than the distance from the target location and prioritize that direction first
        # Only perform an action if start_k == k, meaning that no action has been taken yet in this clock cycle
        if self.start_k == self.k and (abs(current_x - target_x) < abs(current_y - target_y) or current_y == target_y) and  current_x != target_x and current_z != 0: 
            # Distance of the x's is less than the distance of the y's so we will prioritize the x position of the aircraft first given that the current_x is not already at target x and z is not 0
            # This code now either changes the direction of flight or moves the aircraft in the positive or negative x-direction or begins descent if self.landing = "x" and conditions ready
            if self.landing == "x" and abs(current_x - target_x) == current_z and current_y == target_y:
                # self.landing state variable is in 0 or 180 direction and the descent distance is ideal since both x and z change values for descent, and the y-value is the same as the targest destination
                # only will descend if that next descent position is not currently occupied by another aircraft
                # If needed, adjust the direction of flight 
                # If correct direction, then change x-value and decrement z-value
                if current_x < target_x and (current_x + 1, current_y, current_z - 1) not in self.warning_coordinates:
                    # since the current_x is less than the target_x, we need to be in 0 degrees direction, so we either adjust direction angle by factor of 90 or if 0, then increment current_x
                    if self.direction == 0:
                        current_x += 1
                        current_z -= 1
                    elif self.direction == 90:
                        self.direction = 0
                    elif self.direction == 180:
                        self.direction = 90
                    elif self.direction == 270:
                        self.direction = 0
                    
                elif current_x > target_x and (current_x - 1, current_y, current_z - 1) not in self.warning_coordinates:
                    # since the current_x is greater than the target_x, we need to be in 180 degrees direction, so we either adjust direction angle by factor of 90 or if 180, then decrement current_x
                    if self.direction == 0:
                        self.direction = 90
                    elif self.direction == 90:
                        self.direction = 180
                    elif self.direction == 180:
                        current_x -= 1
                        current_z -= 1
                    elif self.direction == 270:
                        self.direction = 180
                # this only executes if the descent position is occupied by another aircraft
                # we want to stay in this position, so we will simply turn the aircraft in a different direction in order for it to turn again in the next round
                else:
                    if self.direction == 0:
                        self.direction = 90
                    elif self.direction == 90:
                        self.direction = 180
                    elif self.direction == 180:
                        self.direction = 270
                    elif self.direction == 270:
                        self.direction = 0

            elif current_x < target_x:
                # if the current x position of the aircraft is less than the target x, then the aircraft should be in the 0 degrees direction
                # if the direction of flight is not already at 0 degrees, then change the direction by a factor of 90 degrees in order to be at 0 degrees or closer to it
                # if the direction of flight was already at 0 degrees from the previous clock cycle, then move the aircraft in the x-direction by incrementing current_x by 1
                if self.direction == 0:
                    current_x += 1
                elif self.direction == 90:
                    self.direction = 0
                elif self.direction == 180:
                    self.direction = 90
                elif self.direction == 270:
                    self.direction = 0
            elif current_x > target_x:
                # if the current x position of the aircraft is greater than the target x, then the aircraft should be in the 180 degrees direction
                # if the direction of flight is not already at 180 degrees, then change the direction by a factor of 90 degrees in order to be at 180 degrees or closer to it
                # if the direction of flight was already at 180 degrees from the previous clock cycle, then move the aircraft in the x-direction by decrementing current_x by 1
                if self.direction == 0:
                    self.direction = 90
                elif self.direction == 90:
                    self.direction = 180
                elif self.direction == 180:
                    current_x -= 1
                elif self.direction == 270:
                    self.direction = 180
            # increment k by 1 to indicate that an action has been performed by the aircraft during this clock cycle
            self.k += 1

        elif self.start_k == self.k and (abs(current_y - target_y) <= abs(current_x - target_x) or current_x == target_x) and current_y != target_y and current_z != 0: 
            # Distance of the y's is less than the distance of the x's so now we prioritize the the y position of the aircraft given that the current_y is not already at target y and z is not 0
            # This code now either changes the direction of flight or moves the aircraft in the positive or negative y-direction
            if self.landing == "y" and abs(current_y - target_y) == current_z and current_x == target_x: 
                # self.landing state variable is in 90 or 270 direction and the descent distance is ideal since both y and z change values for descent, and the x-value is the same as the targest destination
                # only will descend if that next descent position is not currently occupied by another aircraft
                # If needed, adjust the direction of flight 
                # If correct direction, then change y-value and decrement z-value
                if current_y < target_y and (current_x, current_y + 1, current_z - 1) not in self.warning_coordinates:
                    # since the current_y is less than the target_y, we need to be in 90 degrees direction, so we either adjust direction angle by factor of 90 or if 90, then increment current_y
                    if self.direction == 0:
                        self.direction = 90
                    elif self.direction == 90:
                        current_y += 1
                        current_z -= 1
                    elif self.direction == 180:
                        self.direction = 90
                    elif self.direction == 270:
                        self.direction = 0
                elif current_y > target_y and (current_x, current_y - 1, current_z - 1) not in self.warning_coordinates:
                    # since the current_y is greater than the target_y, we need to be in 270 degrees direction, so we either adjust direction angle by factor of 90 or if 270, then decrement current_y
                    if self.direction == 0:
                        self.direction = 270
                    elif self.direction == 90:
                        self.direction = 0
                    elif self.direction == 180:
                        self.direction = 270
                    elif self.direction == 270:
                        current_y -= 1
                        current_z -= 1
                # this only executes if the descent position is occupied by another aircraft
                # we want to stay in this position, so we will simply turn the aircraft in a different direction in order for it to turn again in the next round
                else:
                    if self.direction == 0:
                        self.direction = 90
                    elif self.direction == 90:
                        self.direction = 180
                    elif self.direction == 180:
                        self.direction = 270
                    elif self.direction == 270:
                        self.direction = 0
            elif current_y < target_y:
                # if the current y position of the aircraft is less than the target y, then the aircraft should be in the 90 degrees direction
                # if the direction of flight is not already at 90 degrees, then change the direction by a factor of 90 degrees in order to be at 90 degrees or closer to it
                # if the direction of flight was already at 90 degrees from the previous clock cycle, then move the aircraft in the y-direction by incrementing current_x by 1
                if self.direction == 0:
                    self.direction = 90
                elif self.direction == 90:
                    current_y += 1
                elif self.direction == 180:
                    self.direction = 90
                elif self.direction == 270:
                    self.direction = 0
            elif current_y > target_y:
                # if the current y position of the aircraft is greater than the target y, then the aircraft should be in the 270 degrees direction
                # if the direction of flight is not already at 270 degrees, then change the direction by a factor of 90 degrees in order to be at 270 degrees or closer to it
                # if the direction of flight was already at 270 degrees from the previous clock cycle, then move the aircraft in the y-direction by decrementing current_y by 1
                if self.direction == 0:
                    self.direction = 270
                elif self.direction == 90:
                    self.direction = 0
                elif self.direction == 180:
                    self.direction = 270
                elif self.direction == 270:
                    current_y -= 1
            # increment k by 1 to indicate that an action has been performed by the aircraft during this clock cycle
            self.k += 1


        ##############################
        ## Task J
        ##############################
        # Task that outputs the current x, y, and z values of the current aircraft
        # all output of type int 
        out_x = current_x
        out_y = current_y
        out_z = current_z


        ##############################
        ## Task K
        ##############################
        # check whether the output (x, y, z) is equal to the target destination values
        # if output (x, y, z) = target (x, y, 0), then state variable reached = True which breaks out of the loop (simulating the turning off of this aircraft controller)
        if out_x == target_x and out_y == target_y and out_z == 0:
            self.reached = True
        
        # exit this controller and return the output to the synchronous system in system.py
        return self.reached, out_x, out_y, out_z