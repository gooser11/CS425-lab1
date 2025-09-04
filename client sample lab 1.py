import socket, keyboard, multiprocessing
from time import *

#bfbfbf
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

# works
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
"""
# find interior angle of polygon
def angle(sides):
    if sides < 3:
        raise ValueError("Sides must be more than 2!")
    return (sides - 2) * 180 / sides

# drive in polygon
def polygon(N):
    theta = angle(N)
    print("Angle: ", theta)
    print("Time: ", (1.5 / 90) * theta)

    for i in range(N):
        sock.sendall("a drive_straight(100)".encode())
        print(sock.recv(128).decode())
        sleep(2)
        print("TURN!!!")
        sock.sendall("a spin_right(100)".encode())
        print(sock.recv(128).decode())
        sleep((1.5 / 90) * (180 - theta))


mySides = int(input("Number of sides: "))
polygon(mySides)
"""

#methods to make it easier to read the while loop

def driveForward():
    sock.sendall("a drive_straight(100)".encode()) 
    print(sock.recv(128).decode())   
    sleep(1.5)

def driveBackward():
    sock.sendall("a drive_straight(-100)".encode()) 
    print(sock.recv(128).decode())   
    sleep(1.5)    

def spinLeft():
    sock.sendall("a spin_left(100)".encode())    
    print(sock.recv(128).decode())

def spinRight():
    sock.sendall("a spin_right(100)".encode())    
    print(sock.recv(128).decode())

def stopDrive():
    sock.sendall("a drive_straight(0)".encode())    
    print(sock.recv(128).decode())


# plays song of storms
# works

sock.sendall("a set_song(1, [[62,32],[65,32],[63,32],[62,32],[65,32],[63,32]] )".encode())    
print(sock.recv(128).decode())

# method to play song
def song():
    sock.sendall("a play_song(1)".encode())  
    print(sock.recv(128).decode())
    sleep(8)
# a little dance
def lildance():
    spinRight()
    sleep(3)
    spinLeft()
    sleep(3)
    for i in range(3):
        driveForward()
        sleep(0.2)
        driveBackward()
        sleep(0.2)

if __name__ == "__main__":
    # creating processes
    sing = multiprocessing.Process(target=driveForward, args=(10, ))
    dance = multiprocessing.Process(target=spinLeft, args=(10, ))

    #process 1
    sing.start()
    #process 2
    dance.start()

    sing.join()
    dance.join()
    print("Strafed!")



#remote control done, just tinkering

"""
if __name__ == "__main__":
    # creating processes
    df = multiprocessing.Process(target=driveForward, args=(10, ))
    sl = multiprocessing.Process(target=spinLeft, args=(10, ))
    sr = multiprocessing.Process(target=spinRight, args=(10, ))

#run forever and control robot
timePassed = 50 #value that will be passed as velocity to change speed dynmically
while keyboard.is_pressed == 'w' or keyboard.is_pressed == 'a' or keyboard.is_pressed == 's' or keyboard.is_pressed == 'd':
    key = keyboard.read_key()
    if key == 'w':
        print('Drive forward')
        driveForward()
        timePassed += 1

    elif key == 'a':
        print('Drive left')
        #turn left
        spinLeft()
        timePassed += 1
    
    elif key == 's':
        print('Drive backward')
        driveBackward()
        timePassed += 1

    elif key == 'd':
        print('Drive right')
        #turn right
        spinRight()
        timePassed += 1
    
    elif key == 'q':
        print('Strafe left')
        #process 1
        df.start()
        #process 2
        sl.start()

        df.join()
        sl.join()
        print("Strafed!")


    elif key == 'e':
        print('Strafe right')
        #process 1
        df.start()
        #process 2
        sr.start()

        df.join()
        sr.join()
        print("Strafed!")



    elif not keyboard.is_pressed == 'm' :
        print('Stop')
        stopDrive()
        timePassed = 0

while not keyboard.is_pressed == 'm':
    print('Stopped')
    stopDrive()
    timePassed = 50
"""

sock.sendall("a battery_charge".encode())
print("Battery charge is: ",sock.recv(128).decode())
sock.sendall("a battery_capacity".encode())
print("Battery capacity is: ",sock.recv(128).decode())


""" The c command stops the robot and disconnects.  The stop command will also reset 
the Create's mode to a battery safe PASSIVE.  It is very important to use this command!"""
sock.sendall("c".encode())
print(sock.recv(128).decode())

sock.close()

