import random # used to randomize initial current and target values instead of manual assignments

from controller import Controller # import class Controller from controller.py in same directory


##############################
## Assign Number of Planes
##############################
# Change the value of "n" from 1 to 500 to designate the number of planes in simulation
# max value is 500 to prevent too much congestion since area is 50 km by 50 km
# if exceed 500 planes, it may take a long time to randomly assign unique initial and target positions in 50 km by 50 km area
N = int(input("Number of planes (max is 2500; ideal < 1000 for runtime): "))



################################
## Initial and Target Positions
################################
# This randomizes the initial and target x and y values between the values of  0 and 50 (bounds) 
# Returns two dictionarys:
    # initial_locations = {"plane_#": (initial_x, initial_y, 0), ...} *** all initial_z will be 0 since taking off of ground
    # target_locations = {"plane_#": (target_x, target_y, 0), ...} *** all target_z will be 0 since landing on ground
def random_initials():
    # initial_locations is a dictionary that keeps track of all the initial locations (x, y, z) of all aircrafts in the simulation
    initial_locations = {}
    # target_locations is a dictionary that keeps track of all the target locations (x, y, z) of all aircrafts in the simulation
    target_locations = {}
    # loop through each plane from 1 to N (number of planes)
    for i in range(1, N + 1):
        initial_x, initial_y, target_x, target_y = random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)
        # Assumption that the takeoff and landing destinations must be at least 1 km apart since the initial position != target position
        # This loop ensures that this assumption remains true without having to manually set values each simulation
        while abs(initial_x - target_x) < 1 or abs(initial_y - target_y) < 1:
            if abs(initial_x - target_x) < 1:
                target_x = random.randint(0, 50)
            if abs(initial_y - target_y) < 1:
                target_y = random.randint(0, 50)
        # This loop statement ensures that all current starting locations and target locations is unique. If not, reassign numbers until unique
        while (initial_x, initial_y, 0) in initial_locations.values() or (target_x, target_y) in target_locations.values():
            initial_x, initial_y, target_x, target_y = random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)
            # Assumption that the takeoff and landing destinations must be at least 1 km apart since the initial position != target position
            # This loop ensures that this assumption remains true without having to manually set values each simulation
            while abs(initial_x - target_x) < 1 or abs(initial_y - target_y) < 1:
                if abs(initial_x - target_x) < 1:
                    target_x = random.randint(0, 50)
                if abs(initial_y - target_y) < 1:
                    target_y = random.randint(0, 50)
        # add the unique starting position to initial_locations dictionary for that specific plane
        initial_locations["plane_{0}".format(i)] = (initial_x, initial_y, 0)
        # add the unique target destination to target_locations dictionary for that specific plane
        target_locations["plane_{0}".format(i)] = (target_x, target_y, 0)
    return initial_locations, target_locations


##############################################
## Get Plane Basic Info for Python Purposes
###############################################
# This gets basic plane info to get the Python program to run as a synchronous system
# Returns two data structures:
    # plane_ids = [plane_1, plane_2, ... plane_n] -> list the unique plane_ids for python program to keep track of which controller for what plane is running
    # all_aircrafts = {"plane_#": (x, y, z), ...}  -> dictionary of the input and outputs of individual controllers in the synchronous sytem that each plane_id updates their current value 
def get_plane_info(initial_locations):
    plane_ids = []
    all_aircrafts = {}
    for i in range(1, N + 1):
        plane_ids.append("plane_" + str(i))
        # initial aircraft position is the initial position that was previously calculated
        all_aircrafts["plane_" + str(i)] = initial_locations["plane_" + str(i)]
    return plane_ids, all_aircrafts


##############################################
## Creates different Controller for each plane
###############################################
# This creates a new controller by making a new instance of Controller() from controller.py for each unique plane_id
# Initializes the state variables for that controller, spefically with passing in hte two state variables target_x  and target_y
# Returns list of the memory location of that controller for that plane
def get_controllers(plane_ids, target_locations):
    plane_controllers = []
    for plane in plane_ids:
        target_x, target_y, target_z = target_locations[plane]
        # do not need to have target_z as state variable since lands on ground where z is always 0 
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


    # The synchronous system will keep running until all planes have reached their target destination (aircrafts removed from all_aircrafts when reached)
    while len(all_aircrafts) != 0:
        print("\nNEW CLOCK CYCLE")
        for i, plane in enumerate(plane_controllers):
            plane_id = plane_ids[i]
            if plane_id in all_aircrafts.keys():
                # Runs if that plane_id has not reached its target destination

                # input for that controller is the plane_id in order to retrieve the correct state variables 
                # input is also all_aircrafts in order to see other aircrafts location in vicinity
                # output is all_aircrafts (location of all planes that have not reached target destination)
                all_aircrafts = plane.ClockCycle(plane_id, all_aircrafts)
                
                # print output to the terminal
                print(f"{plane_id}: {all_aircrafts[plane_id]}")

                if all_aircrafts[plane_id] == target_locations[plane_id]:
                    # if that plane_id has reached its targest destination, then remove it from all_aircraft to stop sending location to other aircrafts
                    del all_aircrafts[plane_id]
         
    print("\nAll planes have reached their target destination without collision.")            