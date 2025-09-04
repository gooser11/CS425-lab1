import socket, keyboard
from time import *


# CONFIGURATION PARAMETERS
IP_ADDRESS = "192.168.1.102" 	# SET THIS TO THE RASPBERRY PI's IP ADDRESS
CONTROLLER_PORT = 5001
TIMEOUT = 5				# If its unable to connect after 5 seconds, give up.
                                        # Want this to be a while so robot can initialize.

# connect to the motorcontroller
sock = socket.create_connection( (IP_ADDRESS, CONTROLLER_PORT), TIMEOUT)

""" The t command tests the robot.  It should beep after connecting, move forward 
slightly, then beep on a sucessful disconnect."""
#sock.sendall("t /dev/tty.usbserial-DA01NYDH")			# send a command
#print(sock.recv(128))        # always recieve to confirm that your command was processed

""" The i command will initialize the robot.  It enters the create into FULL mode which
means it can drive off tables and over steps: be careful!"""
sock.sendall("i /dev/ttyUSB0".encode())
print(sock.recv(128).decode())

"""
    Arbitrary commands look like this 
        a *
    Whatever text is given where the * is, is given to the Create API in the form
        result = robot.*
    then any result will be send back.  If there is no result the command will be echoed.
    
    You can see the possible commands here:
    https://github.com/tribelhb/irobot
    
    You may wish to extend the control_server.py on the raspberry pi.
"""


"""
# method that runs roomba in square
def square():
    for i in range(4):
        sock.sendall("a drive_straight(100)".encode())    
        sleep(2)
        sock.sendall("a spin_right(100)".encode())    
        print(sock.recv(128).decode())
        sleep(1.5)
        #sock.sendall("a drive_straight(100)".encode())
# run square
square()
"""

# plays song of storms
"""
sock.sendall("a set_song(1, [[62,32],[65,32],[63,32],[62,32],[65,32],[63,32]] )".encode())    
print(sock.recv(128).decode())

sock.sendall("a play_song(1)".encode())  
print(sock.recv(128).decode())
sleep(8)

"""

# methods to make it easier to read the while loop
def driveForward():
    sock.sendall("a drive_straight(100)".encode()) 
    print(sock.recv(128).decode())   
    #sleep(1.5)

def driveBackward():
    sock.sendall("a drive_straight(-100)".encode()) 
    print(sock.recv(128).decode())   
    #sleep(1.5)    

def spinLeft():
    sock.sendall("a spin_left(100)".encode())    
    print(sock.recv(128).decode())

def spinRight():
    sock.sendall("a spin_right(100)".encode())    
    print(sock.recv(128).decode())

def stopDrive():
    sock.sendall("a drive_straight(0)".encode())    
    print(sock.recv(128).decode())


# run forever and control robot
while True:
    key = keyboard.read_key()
    if key == 'w':
        print('Drive forward')
        driveForward()

    elif key == 'a':
        print('Drive left')
        # turn left
        spinLeft()
    
    elif key == 's':
        print('Drive backward')
        driveBackward()

    elif key == 'd':
        print('Drive right')
        # turn right
        spinRight()
    
    elif key == 'q' :
        print('Stop')
        stopDrive()


sock.sendall("a battery_charge".encode())
print("Battery charge is: ",sock.recv(128).decode())
sock.sendall("a battery_capacity".encode())
print("Battery capacity is: ",sock.recv(128).decode())


""" The c command stops the robot and disconnects.  The stop command will also reset 
the Create's mode to a battery safe PASSIVE.  It is very important to use this command!"""
sock.sendall("c".encode())
print(sock.recv(128).decode())

sock.close()

