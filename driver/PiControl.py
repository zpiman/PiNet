import RPi.GPIO as G
import threading
import time


def isPositive(num):
    return abs(num) == num


class RunListThread(threading.Thread):

    """Class for running the list of instructions independent of all the other code in a thread"""

    def __init__(self, moves, parentRobot, defSpeed, stopEvent):
        threading.Thread.__init__(self)
        self.moves = moves
        self.robot = parentRobot
        self.defSpeed = defSpeed
        self.stopEvent = stopEvent

    def run(self):
        speed = self.defSpeed
        for index in self.moves:
            if self.stopEvent.is_set():
                break
            command = index['command']
            wait_time = index['time']
            drc = 0

            # Comments will be removed (debuging)
            if command == "F":
                self.robot.go(speed, 0)
                drc = 0
                # print("F")
            elif command == "B":
                self.robot.go(speed, 180)
                drc = 180
                # print("B")
            elif command == "R":
                self.robot.go(speed, 90)
                drc = 90
                # print("R")
            elif command == "L":
                self.robot.go(speed, -90)
                drc = -90
                # print("L")
            elif command == "FR":
                self.robot.go(speed, 45)
                drc = 45
                # print("FR")
            elif command == "FL":
                self.robot.go(speed, -45)
                drc = -45
                # print("FL")
            elif command == "BR":
                self.robot.go(speed, 135)
                drc = 135
                # print("BR")
            elif command == "BL":
                self.robot.go(speed, -135)
                drc = -135
                # print("BL")
            elif command == "STOP":
                self.robot.stop()
                # print("STOP")
            elif command == "LIGHTON":
                self.robot.setLight(1)
                # print("LIGHTON")
            elif command == "LIGHTOFF":
                self.robot.setLight(0)
                # print("LIGHTOFF")
            elif command == "S": # change speed, speed 
                speed = int(index['speed'])
                self.robot.go(speed, drc)

            self.stopEvent.wait(wait_time / 1000.0)
        #print("Mission Done...")


class Mission():

    """Class for recording missions"""

    def __init__(self, parentRobot):
        self._Robot = parentRobot
        self.listOfCommands = []
        self.defSpeed = 90
        self.missionStopEv = None
        self.thread = None

    def new(self, comList, defSpeed=90):
        if type(comList) is list:
            self.listOfCommands = comList
        elif type(comList) is dict:
            self.parse(comList)
        self.defSpeed = defSpeed
        return True

    def get(self):
        return self.listOfCommands

    def parse(self, commands):
        # implement
        pass

    def append(self, listToAppend):
        pass

    def run(self, join=False):
        # Start the FUN in a thread
        self.missionStopEv = threading.Event()
        self.thread = RunListThread(
            self.listOfCommands,
            self._Robot,
            self.defSpeed,
            self.missionStopEv)
        self.thread.start()

        if join:
            self.thread.join()

    def stop(self):
        self.missionStopEv.set()


class PiNet:

    """A class for interacting with the Raspberry Pi Robot"""

    def __init__(self, pins, freq=50, board=G.BOARD):

        G.setmode(board)  # initialization of GPIO ports
        G.setup(pins['RightFront'], G.OUT)
        G.setup(pins['RightBack'], G.OUT)
        G.setup(pins['LeftFront'], G.OUT)
        G.setup(pins['LeftBack'], G.OUT)

        G.setup(pins['Light'], G.OUT)
        G.setup(pins['Laser'], G.OUT)

        G.setup(pins['ServoH'], G.OUT)
        G.setup(pins['ServoV'], G.OUT)
        
        # set up pin refs
        self.pins = pins
        self.frequency = freq
        
        # keep track of the status of the components
        self.component = {
            "light": False,
            "laser": False
        }
        
        # The X, Y times for servos
        self.ServoTimesHV = [1.35, 1.35]

        # The time range for servos
        self.ServoRange = [0.68, 1.95]
        
        # array of pins
        self.pinArray = {
            "RightFront": G.PWM(self.pins["RightFront"], self.frequency),
            "RightBack": G.PWM(self.pins["RightBack"], self.frequency),
            "LeftFront": G.PWM(self.pins["LeftFront"], self.frequency),
            "LeftBack": G.PWM(self.pins["LeftBack"], self.frequency)
        }
    
    # update the speen and direction of the robot
    def go(self, speed, direction):
        rightM = 0
        leftM = 0
        if direction == 0:
            rightM = 100
            leftM = 100
        elif direction == 45:
            rightM = 50
            leftM = 100
        elif direction == -45:
            rightM = 100
            leftM = 50
        elif direction == 90:
            rightM = -80
            leftM = 80
        elif direction == -90:
            rightM = 80
            leftM = -80
        elif direction == 135:
            rightM = -50
            leftM = -100
        elif direction == -135:
            rightM = -100
            leftM = -50
        elif abs(direction) == 180:
            rightM = -100
            leftM = -100

        speed = speed / 100.0
        rightM = rightM * speed
        leftM = leftM * speed

        if isPositive(rightM):
            self.pinArray["RightBack"].stop()
            self.pinArray["RightFront"].start(rightM)
        else:
            self.pinArray["RightFront"].stop()
            self.pinArray["RightBack"].start(abs(rightM))

        if isPositive(leftM):
            self.pinArray["LeftBack"].stop()
            self.pinArray["LeftFront"].start(leftM)
        else:
            self.pinArray["LeftFront"].stop()
            self.pinArray["LeftBack"].start(abs(leftM))
    
    # Stop the robot
    def stop(self):
        for key in self.pinArray:
            self.pinArray[key].stop() # Stop the PWM on each output pins
    
    # Set the light to a given state
    def setLight(self, state):
        self.component["light"] = state
        G.output(self.pins["Light"], int(state))

    # get the status of the light
    def getLight(self):
        return self.component["light"]
    
    # Set the laser to a state
    def setLaser(self, state):
        self.component["laser"] = state
        G.output(self.pins["Laser"], int(state))
    
    # get the status of the laser
    def getLaser(self):
        return self.component["laser"]
    
    # start a mission
    def startMission(self):
        pass

    # stop a mission
    def stopMission(self):
        pass
    
    # change the cam to a new state
    def changeCam(self, state):

        if not state == [0, 0, 0, 0]:

            msH = 0
            msV = 0
            if len(state) == 4:
                if state[0] == "1" and self.ServoTimesHV[1] >= self.ServoRange[0]:
                    self.ServoTimesHV[1] -= 0.05
                    self.changeServo(self.pins["ServoV"], self.ServoTimesHV[1])

                if state[1] == "1" and self.ServoTimesHV[0] <= self.ServoRange[1]:
                    self.ServoTimesHV[0] += 0.05
                    self.changeServo(self.pins["ServoH"], self.ServoTimesHV[0])

                if state[2] == "1" and self.ServoTimesHV[1] <= self.ServoRange[1]:
                    self.ServoTimesHV[1] += 0.05
                    self.changeServo(self.pins["ServoV"], self.ServoTimesHV[1])

                if state[3] == "1" and self.ServoTimesHV[0] >= self.ServoRange[0]:
                    self.ServoTimesHV[0] -= 0.05
                    self.changeServo(self.pins["ServoH"], self.ServoTimesHV[0])

            else:
                msH = 1.3
                msV = 1.3

                self.changeServo(self.pins["ServoH"], msH)
                self.changeServo(self.pins["ServoV"], msV)
    
    # Update the servos
    def changeServo(self, servo, ms):
        # TODO: Must run in a separate thread
        G.output(servo, 1)
        time.sleep(ms / 1000)
        G.output(servo, 0)
    
    # clean up
    def closeMe(self):
        G.cleanup()

if __name__ == "__main__":
    PINS = {
        "RightFront": 11,
        "RightBack": 12,
        "LeftFront": 13,
        "LeftBack": 15,
        "Light": 23,
        "Laser": 19,
        "ServoH": 18,
        "ServoV": 16
    }
    robot = PiNet(PINS)
    robot.changeCam("default")

    #mission = Mission(robot)
    #mission.new([("F", 2000),("F",500),("STOP",1000),("LIGHTON",0),("F",5000),("F",5000),("LIGHTOFF",2000),("R",3000)])
    # mission.run(True)

    #print("About to close")
    robot.closeMe()
