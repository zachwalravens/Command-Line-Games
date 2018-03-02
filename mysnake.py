import time, sys, select, os, threading


#array = [[" "," "," "," "," ",],
#         [" "," "," "," "," ",],
#         [" "," "," "," "," ",],
#         [" "," "," "," "," ",],
#         [" "," "," "," "," ",]]

class Traveler(object):

    start = 0
    char = ""
    arr = []

    def __init__(self, start, char, arr):
        self.start = start
        self.char = char
        self.arr = arr

    def update(self, i):
        i = i % (len(self.arr)*len(self.arr[0]))
        arrWidth = len(self.arr[0])
        self.arr[(i-self.start-1)/arrWidth][(i-self.start-1)%arrWidth] = str(" ")
        self.arr[(i-self.start)/arrWidth][(i-self.start)%arrWidth] = self.char

    def show(self, i, isHorizontal):
        i = i % (len(self.arr)*len(self.arr[0]))
        if isHorizontal:
            arrWidth = len(self.arr[0])
            self.arr[(-1*self.start)/arrWidth][(-1*self.start)%arrWidth] = self.char
        else:
            arrWidth = len(self.arr)
            self.arr[(-1*self.start)%arrWidth][(-1*self.start)/arrWidth] = self.char  
        return self

    def preRemove(self, i, isHorizontal):
        i = i % (len(self.arr)*len(self.arr[0]))
        if isHorizontal:
            arrWidth = len(self.arr[0])
            self.arr[(-1*self.start)/arrWidth][(-1*self.start)%arrWidth] = " "
        else:
            arrWidth = len(self.arr)
            self.arr[(-1*self.start)%arrWidth][(-1*self.start)/arrWidth] = " "           
        return self

    def getArray(self):
        return self.arr

class TravelerGroup(object):

    char = "X"
    startLength = 1
    arr = []
    addIsHorizontal = True
    deleteIsHorizontal = True

    travelersArray = []
    currentTravelerStartNum = 0
    afterFlipI = -7

    def __init__(self, arr, char="X", startLength=1):
        self.arr = arr
        self.char = char
        self.startLength = startLength

        while self.currentTravelerStartNum < startLength:
            self.travelersArray.append(Traveler(self.currentTravelerStartNum, self.char, self.arr))
            self.currentTravelerStartNum += 1

        for each in self.travelersArray:
            each.update(0)

    def addTraveler(self):
        self.travelersArray.append(Traveler(self.currentTravelerStartNum, self.char, self.arr))
        self.currentTravelerStartNum += 1

    def update(self, i):
        #for each in self.travelersArray:
        #    each.update(i)

        # Removes last element of travelers array
        self.travelersArray.remove(self.travelersArray[len(self.travelersArray) - 1].preRemove(i, self.deleteIsHorizontal))
        # Adds new element to start
        self.travelersArray.insert(0, Traveler(-1*i - 1, self.char, self.arr).show(i, self.addIsHorizontal))

        if not mainTravelerGroup.addIsHorizontal and mainTravelerGroup.deleteIsHorizontal and i == self.afterFlipI + len(self.travelersArray) - 1:
            mainTravelerGroup.deleteIsHorizontal = False


    def turnToDown(self, i):
        mainTravelerGroup.addIsHorizontal = False
        i = flipStart(i, 40)
        self.afterFlipI = i
        return i



def createArr(width, height, char):
    arr = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(char)
        arr.append(row)
    return arr


def conCarArray(arr):
    str = ""
    for ch in arr:
        str += ch
    return str

def conCarArrayVert(arr):
    str = ""
    for each in arr:
        str += conCarArray(each) + "\n"
    return str

def flipStart(num, width):
    return (num % width)*width + (num/width)

def restartPrint(stringInput):
    sys.stdout.write("\r" + stringInput)
    sys.stdout.flush()

width = 40
height = 40

array = createArr(width, height, " ")

mainTravelerGroup = TravelerGroup(array, "X", 5)

i = 0
while i < width*height*10:

    if i % width == 0:
        mainTravelerGroup.addTraveler()

    #if i == 60:
    #    mainTravelerGroup.addIsHorizontal = False
    #    i = flipStart(i, width)
    #    afterFlipI = i
    #if not mainTravelerGroup.addIsHorizontal and mainTravelerGroup.deleteIsHorizontal and i == afterFlipI + len(mainTravelerGroup.travelersArray):
    #    mainTravelerGroup.deleteIsHorizontal = False
    if i == 20:
        i = mainTravelerGroup.turnToDown(i)

    mainTravelerGroup.update(i)


    os.system("clear")
    print(conCarArrayVert(array))
    print("Score: " + str(len(mainTravelerGroup.travelerArray)) + "  Streak: " + str(mainTravelerGroup.streakScore))
    time.sleep(mainTravelerGroup.getSleepTime())

    i += 1