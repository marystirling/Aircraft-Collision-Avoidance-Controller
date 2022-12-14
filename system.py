import random # used to randomize initial current and target values instead of manual assignments

from controller import Controller # import class Controller from controller.py in same directory


##############################
## Assign Number of Planes
##############################
# Change the value of "n" from 1 to max?? to designate the number of planes in simulation
# TODO: change this as the input later on to be more interactive
n = 15



################################
## Initial and Target Positions
################################
# This randomizes the initial and target x and y values between the values of  0 and 30 (bounds) 
# Returns two dictionarys:
    # current_locations = {"plane_#": (current_x, current_y, current_z), ...}
    # target_locations = {"plane_#": (target_x, target_y), ...} *** all target_z will be 0 since landing on ground
def random_initials():
    # current_locations is a dictionary that keeps track of all the current locations (x, y, z) of all aircrafts in the simulation
    current_locations = {}
    # target_locations is a dictionary that keeps track of all the target locations (x, y, z) of all aircrafts in the simulation
    target_locations = {}
    # loop through each plane from 1 to n (number of planes)
    for i in range(1, n + 1):
        current_x, current_y, target_x, target_y = random.randint(0, 30), random.randint(0, 30), random.randint(0, 30), random.randint(0, 30)
        current_z = 0
        print(f"curr_x {current_x}, target_x {target_x}, current_y {current_y}, target_y {target_y}")
        # Assumption that the takeoff and landing destinations must be at least 1 km apart since the initial position != target position
        # This loop ensures that this assumption remains true without having to manually set values each simulation
        while abs(current_x - target_x) < 1 or abs(current_y - target_y) < 1:
            print(f"current_x {current_x}, target_x {target_x}, current_y {current_y}, target_y {target_y}")
            if abs(current_x - target_x) < 1:
                target_x = random.randint(0, 30)
            if abs(current_y - target_y) < 1:
                target_y = random.randint(0, 30)
        # This loop statement ensures that all current starting locations and target locations is unique. If not, reassign numbers until unique
        while (current_x, current_y, current_z) in current_locations.values() or (target_x, target_y) in target_locations.values():
            current_x, current_y, target_x, target_y = random.randint(0, 30), random.randint(0, 30), random.randint(0, 30), random.randint(0, 30)
            current_z = 0
            # Assumption that the takeoff and landing destinations must be at least 1 km apart since the initial position != target position
            # This loop ensures that this assumption remains true without having to manually set values each simulation
            while abs(current_x - target_x) < 1 or abs(current_y - target_y) < 1:
                print(f"current_x {current_x}, target_x {target_x}, current_y {current_y}, target_y {target_y}")
                if abs(current_x - target_x) < 1:
                    target_x = random.randint(0, 30)
                if abs(current_y - target_y) < 1:
                    target_y = random.randint(0, 30)
        # add the unique current starting position to current_locations dictionary for that specific plane
        current_locations["plane_{0}".format(i)] = (current_x, current_y, current_z)
        # add the unique target destination to target_locations dictionary for that specific plane
        target_locations["plane_{0}".format(i)] = (target_x, target_y)
    return current_locations, target_locations


##############################################
## Get Plane Basic Info for Python Purposes
###############################################
# This gets basic plane info to get the Python program to run as a synchronous system
# Returns two data structures:
    # all_reached = {"plane_#": False, ...}  -> for the synchronous system to see when all planes have reached the target destination to "turn off" system
    # plane_ids = [plane_1, plane_2, ... plane_n] -> list the unique plane_ids for python program to keep track of which controller for what plane is running
def get_plane_info():
    plane_ids = []
    all_reached = {}
    for i in range(1, n + 1):
        all_reached["plane_" + str(i)] = False
        plane_ids.append("plane_" + str(i))
    return plane_ids, all_reached


##############################################
## Creates different Controller for each plane
###############################################
# This creates a new controller by making a new instance of Controller() from controller.py for each unique plane_id
# Instantiates the state variables for that controller by plane.__init__() 
# Returns list of the memory location of that controller for that plane
def get_controllers(plane_ids):
    plane_controllers = []
    for plane in plane_ids:
        plane = Controller()
        plane.__init__()
        plane_controllers.append(plane)
    return plane_controllers



##############################################
## Synchronous System
###############################################
# Models the synchronous system by creating a feedback loop for all the controllers for the n planes
if __name__ == '__main__':
    current_locations, target_locations = random_initials()
    plane_ids, all_reached = get_plane_info()
    plane_controllers = get_controllers(plane_ids)

    other_aircraft = {}

    # The synchronous system will keep running until all planes have reached their target destination
    while not all(value == True for value in all_reached.values()):
        for i, plane in enumerate(plane_controllers):
            target_x, target_y = target_locations[plane_ids[i]]
            current_x, current_y, current_z = current_locations[plane_ids[i]]
            if all_reached[plane_ids[i]] == False:
                # Runs if that plane_id has not reached its target destination
                print(f"\nPLANE RUNNING IS {plane_ids[i]}")
                if plane_ids[i] in other_aircraft.keys():
                    del other_aircraft[plane_ids[i]]
                # input for that controller with plane_id with the correct inputs as arguments and the returned variables as the output
                reached, out_x, out_y, out_z = plane.ClockCycle(current_x, current_y, current_z, target_x, target_y, other_aircraft)
                # update the current location of that plane_id so that it can be the input for the next clock cycle for that controller
                current_locations[plane_ids[i]] = (out_x, out_y, out_z)
                other_aircraft[plane_ids[i]] = (out_x, out_y, out_z)
                if reached == True:
                    # if that plane_id has reached its targest destination, then change its value as True in all_reached
                    # we then want to take that plane_id out of messaging its location with other plane_id
                    del other_aircraft[plane_ids[i]]
                    all_reached[plane_ids[i]] = True
    print("All planes have reached their target destination without collision.")            