import random # used to randomize initial current and target values instead of manual assignments
#import controller
from controller import Controller
#from controller import init


##############################
## Assign Number of Planes
##############################
# Change the value of "n" from 1 to max?? to designate the number of planes in simulation
# TODO: change this as the input later on to be more interactive
n = 1



##############################
## Initial and Target Positions
##############################
# This randomizes the initial and target x and y values between the values of  0 and 30 (bounds) 
def random_initials():
    # current_locations is a dictionary that keeps track of all the current locations (x, y, z) of all aircrafts in the simulation
    current_locations = {}

    # target_locations is a dictionary that keeps track of all the target locations (x, y, z) of all aircrafts in the simulation
    target_locations = {}
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
        current_locations["plane_{0}".format(i)] = (current_x, current_y, current_z)
        target_locations["plane_{0}".format(i)] = (target_x, target_y)
    return current_locations, target_locations

def get_plane_info():
    plane_ids = []
    all_reached = {}
    for i in range(1, n + 1):
        all_reached["plane_" + str(i)] = False
        plane_ids.append("plane_" + str(i))
    return plane_ids, all_reached

def get_controllers(plane_ids):
    plane_controllers = []
    for plane in plane_ids:
        plane = Controller()
        plane.__init__()
        plane_controllers.append(plane)
        return plane_controllers

current_locations, target_locations = random_initials()
plane_ids, all_reached = get_plane_info()
plane_controllers = get_controllers(plane_ids)



while all(value == False for value in all_reached.values()):
    for i, plane in enumerate(plane_controllers):
        target_x, target_y = target_locations[plane_ids[i]]
        current_x, current_y, current_z = current_locations[plane_ids[i]]
        reached, current_x, current_y, current_z = plane.ClockCycle(current_x, current_y, current_z, target_x, target_y)
        current_locations[plane_ids[i]] = (current_x, current_y, current_z)
        if reached == True:
            all_reached[plane_ids[i]] = True
        
