import random # used to randomize initial current and target values instead of manual assignments

from controller import Controller # import class Controller from controller.py in same directory


##############################
## Assign Number of Planes
##############################
# Change the value of "n" from 1 to 500 to designate the number of planes in simulation
# max value is 500 to prevent too much congestion since area is 50 km by 50 km
# if exceed 500 planes, it may take a long time to randomly assign unique initial and target positions in 50 km by 50 km area
#n = int(input("Enter the number of planes to run in the simulation (max is 500): "))
N = 50


################################
## Initial and Target Positions
################################
# This randomizes the initial and target x and y values between the values of  0 and 50 (bounds) 
# Returns two dictionarys:
    # current_locations = {"plane_#": (initial_x, initial_y, initial_z), ...}
    # target_locations = {"plane_#": (target_x, target_y), ...} *** all target_z will be 0 since landing on ground
def random_initials():
    # current_locations is a dictionary that keeps track of all the current locations (x, y, z) of all aircrafts in the simulation
    initial_locations = {}
    # target_locations is a dictionary that keeps track of all the target locations (x, y, z) of all aircrafts in the simulation
    target_locations = {}
    # loop through each plane from 1 to n (number of planes)
    for i in range(1, N + 1):
        initial_x, initial_y, target_x, target_y = random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)
        initial_z = 0
        # Assumption that the takeoff and landing destinations must be at least 1 km apart since the initial position != target position
        # This loop ensures that this assumption remains true without having to manually set values each simulation
        while abs(initial_x - target_x) < 1 or abs(initial_y - target_y) < 1:
            print(f"initial_x {initial_x}, target_x {target_x}, initial_y {initial_y}, target_y {target_y}")
            if abs(initial_x - target_x) < 1:
                target_x = random.randint(0, 50)
            if abs(initial_y - target_y) < 1:
                target_y = random.randint(0, 50)
        # This loop statement ensures that all current starting locations and target locations is unique. If not, reassign numbers until unique
        while (initial_x, initial_y, initial_z) in initial_locations.values() or (target_x, target_y) in target_locations.values():
            initial_x, initial_y, target_x, target_y = random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)
            initial_z = 0
            # Assumption that the takeoff and landing destinations must be at least 1 km apart since the initial position != target position
            # This loop ensures that this assumption remains true without having to manually set values each simulation
            while abs(initial_x - target_x) < 1 or abs(initial_y - target_y) < 1:
                print(f"initial_x {initial_x}, target_x {target_x}, initial_y {initial_y}, target_y {target_y}")
                if abs(initial_x - target_x) < 1:
                    target_x = random.randint(0, 50)
                if abs(initial_y - target_y) < 1:
                    target_y = random.randint(0, 50)
        # add the unique current starting position to current_locations dictionary for that specific plane
        initial_locations["plane_{0}".format(i)] = (initial_x, initial_y, initial_z)
        # add the unique target destination to target_locations dictionary for that specific plane
        # do not need target_z since it is always 0 since on ground
        target_locations["plane_{0}".format(i)] = (target_x, target_y, 0)
    return initial_locations, target_locations


##############################################
## Get Plane Basic Info for Python Purposes
###############################################
# This gets basic plane info to get the Python program to run as a synchronous system
# Returns two data structures:
    # all_reached = {"plane_#": False, ...}  -> for the synchronous system to see when all planes have reached the target destination to "turn off" system
    # plane_ids = [plane_1, plane_2, ... plane_n] -> list the unique plane_ids for python program to keep track of which controller for what plane is running
def get_plane_info(initial_locations):
    plane_ids = []
    all_aircrafts = {}
    for i in range(1, N + 1):
        plane_ids.append("plane_" + str(i))
        all_aircrafts["plane_" + str(i)] = initial_locations["plane_" + str(i)]
    return plane_ids, all_aircrafts


##############################################
## Creates different Controller for each plane
###############################################
# This creates a new controller by making a new instance of Controller() from controller.py for each unique plane_id
# Initializes the state variables for that controller by plane.__init__() 
# Returns list of the memory location of that controller for that plane
def get_controllers(plane_ids, target_locations):
    plane_controllers = []
    for plane in plane_ids:
        target_x, target_y, target_z = target_locations[plane]
        plane = Controller(target_x, target_y)
        plane_controllers.append(plane)
    return plane_controllers



##############################################
## Synchronous System
###############################################
# Models the synchronous system by creating a feedback loop for all the controllers for the n planes
if __name__ == '__main__':


    # functions to set up the synchronous system for amount of planes chosen
    initial_locations, target_locations = random_initials()
    plane_ids, all_aircrafts = get_plane_info(initial_locations)
    plane_controllers = get_controllers(plane_ids, target_locations)

    # dictionary to keep track of the other locations (x,y,z) for a specific plane id
    # used as input for each controller so the current aircraft can know where other aircraft are
    # starts as an initial list, but will be other_aircraft = {"plane_1": (x, y, z), ..., "plane_n": (x, y, z)}

    # The synchronous system will keep running until all planes have reached their target destination
    #while not all(value == True for value in all_reached.values()):
    while len(all_aircrafts) != 0:
        print("\nNEW CLOCK CYCLE")
        for i, plane in enumerate(plane_controllers):
            plane_id = plane_ids[i]

            if plane_id in all_aircrafts.keys():
                # Runs if that plane_id has not reached its target destination
                # want to remove the current plane's location from other_aircraft for this clock cycle 

                # input for that controller with plane_id with the correct inputs as arguments and the returned variables as the output
                all_aircrafts = plane.ClockCycle(plane_id, all_aircrafts)
                
                # print output to the terminal
                print(f"{plane_id}: {all_aircrafts[plane_id]}")

                if all_aircrafts[plane_id] == target_locations[plane_id]:
                    # if that plane_id has reached its targest destination, then change its value as True in all_reached
                    # we then want to take that plane_id out of messaging its location with other plane_id
                    #del other_aircraft[plane_id]
                    del all_aircrafts[plane_id]
                    #all_reached[plane_id] = True
    print("\nAll planes have reached their target destination without collision.")            