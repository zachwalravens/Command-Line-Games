import time, sys, select, os, pygame, random, time
from threading import Thread

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

def directionToX(direction):
    if direction == Direction.DOWN or direction == Direction.UP:
        return 0
    if direction == Direction.RIGHT:
        return 1
    if direction == Direction.LEFT:
        return -1

def directionToY(direction):
    if direction == Direction.LEFT or direction == Direction.RIGHT:
        return 0
    if direction == Direction.DOWN:
        return 1
    if direction == Direction.UP:
        return -1

class Direction(enumerate):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Traveler(object):

    x = 0
    y = 0
    char = "X"
    arr = []

    def __init__(self, x, y, char, arr):
        self.x = x
        self.y = y
        self.char = char
        self.arr = arr

    def show(self):
        self.arr[self.y][self.x] = "X"
        return self

    def preRemove(self):
        self.arr[self.y][self.x] = " "
        return self


class TravelerGroup(object):

    char = "X"
    startLength = 1
    moveDirection = Direction.RIGHT
    arr = []

    addX = 0
    addY = 0

    travelerArray = []

    def __init__(self, char, startLength, moveDirection, arr, addX, addY):
        self.speed = 10
        self.char = char
        self.startLength = startLength
        self.moveDirection = moveDirection
        self.arr = arr
        self.streakScore = 1
        self.travelersToAdd = 0

        self.addX = addX
        self.addY = addY

        for i in range(startLength):
            self.addTraveler()

    def addTraveler(self):
        self.travelerArray.append(Traveler(self.addX, self.addY, self.char, self.arr).show())
        self.addX = (self.addX + directionToX(self.moveDirection)) % len(self.arr[0])
        self.addY = (self.addY + directionToY(self.moveDirection)) % len(self.arr)

    def removeFirstTraveler(self):
        self.travelerArray.remove(self.travelerArray[0].preRemove())

    def move(self):
        self.addTraveler()
        if self.travelersToAdd <= 0:
            self.removeFirstTraveler()
        else:
            self.travelersToAdd -= 1

    def longerAndFaster(self):
        self.addTraveler()
        self.speed += 1

    def checkForSpecialPixel(self):
        for each in self.travelerArray:
            if each.x == self.addX and each.y == self.addY:
                self.selfIntersection()
        if self.arr[self.addY][self.addX] == "O":
            self.consumeFood(self.addX, self.addY)
        
    def selfIntersection(self):
        print("Your score was " + str(len(self.travelerArray)))
        os._exit(0)

    def getSleepTime(self):
        if self.moveDirection == Direction.LEFT or self.moveDirection == Direction.RIGHT:
            return 0.5/self.speed
        if self.moveDirection == Direction.UP or self.moveDirection == Direction.DOWN:
            return 1.0/self.speed

    def consumeFood(self, x, y):
        self.arr[y][x] = " "
        self.travelersToAdd += self.streakScore
        self.streakScore += 1

        for each in foodArr:
            if x == each[0] and y == each[1]:
                foodArr.remove(each)

def addFood(arr):
    width = len(arr[0])
    height = len(arr)

    x = int(random.random()*width)
    y = int(random.random()*height)

    if arr[y][x] == " ":
        arr[y][x] = "O"
        foodArr.append([x,y])
    else:
        addFood(arr)


random.seed(time.time())
array = createArr(40, 20, " ")
foodArr = []
mainTravelerGroup = TravelerGroup("X", 5, Direction.RIGHT, array, 0, 0)

pygame.init()

i = 0
while True:
    for event in pygame.event.get():
        if event.type in (pygame.KEYDOWN, pygame.KEYUP) and event.key == pygame.K_UP and mainTravelerGroup.moveDirection != Direction.DOWN:
            mainTravelerGroup.moveDirection = Direction.UP
            break
        if event.type in (pygame.KEYDOWN, pygame.KEYUP) and event.key == pygame.K_RIGHT and mainTravelerGroup.moveDirection != Direction.LEFT:
            mainTravelerGroup.moveDirection = Direction.RIGHT
            break
        if event.type in (pygame.KEYDOWN, pygame.KEYUP) and event.key == pygame.K_DOWN and mainTravelerGroup.moveDirection != Direction.UP:
            mainTravelerGroup.moveDirection = Direction.DOWN
            break
        if event.type in (pygame.KEYDOWN, pygame.KEYUP) and event.key == pygame.K_LEFT and mainTravelerGroup.moveDirection != Direction.RIGHT:
            mainTravelerGroup.moveDirection = Direction.LEFT
            break

    if i % (mainTravelerGroup.speed*2) == 0:
        addFood(array)

    if i % (mainTravelerGroup.speed*4) == 0:    
        if mainTravelerGroup.streakScore > 1:
            mainTravelerGroup.streakScore -= 1

    if len(foodArr) > 20:
        print("The board has been infested. Game over")
        print("Score: " + str(len(mainTravelerGroup.travelerArray)))
        os._exit(0)

    mainTravelerGroup.checkForSpecialPixel()
    mainTravelerGroup.move()

    os.system("clear")
    print(conCarArrayVert(array))
    print("Score: " + str(len(mainTravelerGroup.travelerArray)) + "  Streak: " + str(mainTravelerGroup.streakScore) + " Zergs Until Infestation: " + str(21 - len(foodArr)))
    time.sleep(mainTravelerGroup.getSleepTime())

    i += 1