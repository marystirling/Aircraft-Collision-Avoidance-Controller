# CPS_Final_Aircraft_Collision_Avoidance_System

Code by:\
Mary Stirling Brown\
Vanderbilt University\
CS 6376-01 Hybrid/Embedded Systems\
Final Project

Code runs on Windows, Mac, and Linux machines

### Python Version and Imports
Python version: 3.9.9\
Needed import modules: random

### Download Code
```
git clone https://github.com/marystirling/Aircraft-Collision-Avoidance-Controller.git
```

### Run Code
In terminal, go to the directory with downloaded code. Make sure that controller.py and system.py are located in the same directory.\
Next, execute one of the following commands depending what python is downloaded on machine:
```
python system.py
```
```
python3 system.py
```
It will ask for an input. Please input the number of desired aircrafts you want to run in the simulation. The minimum is 1. The maximum is 2500 since it only runs in 50x50 coordinate space. For best runtime, choose the number to be less than 1000. If run with 2500 aircrafts, it could take approximately 3-10 minutes to finish running since the flying area is very congested with aircraft traffic.
