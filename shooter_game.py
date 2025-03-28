import time, sys, select, os, pygame, random, time
from enum import Enum

STARTING_SHOTS = 20
JUMP_RADIUS = 0.5
SHOTS_FOR_KILL = 1
ATTACKER_VERTICAL_SPEED = 0.5
ATTACKER_HORIZONTAL_SPEED = 1.0

currentAttackerVerticalSpeed = ATTACKER_VERTICAL_SPEED
currentAttackerHorizontalSpeed = ATTACKER_HORIZONTAL_SPEED

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

class MovementType(Enum):
    SINGLE = 1
    AUTO = 2

attackerArray = []

def findAttackers(y, x):
    arr = []
    for each in attackerArray:
        if int(each.currentX) == x and int(each.currentY) == y:
            arr.append(each)
    return arr


class PowerUp(object):

    X = 0
    Y = 0
    symbol = "A"
    arr = []

    def __init__(self, X, Y, symbol, arr):
        self.X = X
        self.Y = Y
        self.symbol = symbol
        self.arr = arr
    
    def show(self):
        if self.arr[self.Y][self.X] == " ":
            self.arr[self.Y][self.X] = self.symbol

    def useAndRemove(self):
        doPowerUp(self.symbol)
        self.arr[self.Y][self.X] = " "
        return self


class Particle(object):

    currentX = 0
    currentY = 0
    symbol = "X"
    arr = []
    invincible = False

    projectileArr = []

    def __init__(self, currentX, currentY, symbol, arr):
        self.currentX = currentX
        self.currentY = currentY
        self.dx = 0
        self.dy = 0
        self.symbol = symbol
        self.arr = arr

        self.shotsLeft = STARTING_SHOTS
        self.score = 0

        self.stillMoving = True

        self.arr[currentY][currentX] = symbol

    def move(self, depth):
        if self.stillMoving:
            if depth == 1:
                useAndRemovePowerUp(int(self.currentX), int(self.currentY))

            if self.arr[int(self.currentY)][int(self.currentX)] == "O" and depth == 1 and (not self.invincible): #Killed by attacker
                os._exit(0)
            if self.arr[int(self.currentY)][int(self.currentX)] == "O" and depth == 1 and self.invincible: #Kills Attacker While Invinvible
               for each in findAttackers(int(self.currentY), int(self.currentX)):
                    each.die()    
            if self.arr[int(self.currentY)][int(self.currentX)] == "O" and depth == 0: # Projectile kills attacker
                for each in findAttackers(int(self.currentY), int(self.currentX)):
                    each.die()

            self.arr[int(self.currentY)][int(self.currentX)] = " "

            if depth == 1: # Player Case
                self.currentY = (self.currentY + self.dy)
                if self.currentY >= len(self.arr):
                    self.currentY = len(self.arr) - 1
                if self.currentY < 0:
                    self.currentY = 0
                self.currentX = (self.currentX + self.dx)
                if self.currentX >= len(self.arr[0]):
                    self.currentX = len(self.arr[0]) - 1
                if self.currentX < 0:
                    self.currentX = 0
            elif depth == 0: # Projectile Case
                self.currentY = (self.currentY + self.dy)
                self.currentX = (self.currentX + self.dx)

            if self.currentX < len(self.arr[0]) and self.currentY < len(self.arr) and self.currentX > 0.0 and self.currentY > 0.0:
                self.arr[int(self.currentY)][int(self.currentX)] = self.symbol
            elif depth == 0:
                self.stillMoving = False

            if depth > 0:
                for each in self.projectileArr:
                    if each.stillMoving:
                        each.move(depth - 1)
                    else:
                        self.projectileArr.remove(each)

    def shootProjectile(self, dx, dy):
        if not(dx == 0.0 and dy == 0.0) and self.shotsLeft > 0:
            self.projectileArr.append(Particle(self.currentX, self.currentY, "*", self.arr))
            self.projectileArr[len(self.projectileArr) - 1].dx = dx
            self.projectileArr[len(self.projectileArr) - 1].dy = dy
            self.shotsLeft -= 1

    def giveShots(self, howMany):
        self.shotsLeft += howMany

    def increaseScore(self, howMany):
        self.score += howMany

class Attacker(object):

    currentX = 0
    currentY = 0
    dx = 0.0
    dy = 0.0
    symbol = "O"
    arr = []
    dead = False

    target = Particle(0,0,"",[[""]])

    def __init__(self, currentX, currentY, symbol, target, arr):
        self.currentX = currentX
        self.currentY = currentY
        self.symbol = symbol
        self.arr = arr

        self.target = target

    def die(self):
        self.arr[int(self.currentY)][int(self.currentX)] = " "
        symbol = " "
        self.dead = True
        self.target.giveShots(SHOTS_FOR_KILL)
        self.target.increaseScore(1)

    def move(self):
        if not self.dead:
            if self.arr[int(self.currentY)][int(self.currentX)] == "O": # Normal
                self.arr[int(self.currentY)][int(self.currentX)] = " "
            elif self.arr[int(self.currentY)][int(self.currentX)] == "*": # Gets shot
                self.die()
            elif self.arr[int(self.currentY)][int(self.currentX)] == "X" and (not thisPlayer.invincible): # Kills player
                os._exit(0)
            elif self.arr[int(self.currentY)][int(self.currentX)] == "X" and thisPlayer.invincible: #Kills Attacker While Invinvible
                self.die()

            distance = ((self.currentX - self.target.currentX)**2 + (self.currentY - self.target.currentY)**2)**0.5

            if distance > JUMP_RADIUS: # Moves
                self.dx = currentAttackerHorizontalSpeed*(self.target.currentX - self.currentX)/distance
                self.dy = currentAttackerVerticalSpeed*(self.target.currentY - self.currentY)/distance

                self.currentY = (self.currentY + self.dy)
                if random.random() < 0.15:
                    self.currentY += + (random.random()*2 - 1)*currentAttackerVerticalSpeed
                self.currentX = (self.currentX + self.dx)
                if random.random() < 0.15:
                    self.currentX += + (random.random()*2 - 1)*currentAttackerHorizontalSpeed
            else: # Jumps on Player
                self.currentX = self.target.currentX
                self.currentY = self.target.currentY

            if self.currentX < len(self.arr[0]) and self.currentY < len(self.arr) and self.currentX > 0.0 and self.currentY > 0.0:
                self.arr[int(self.currentY)][int(self.currentX)] = self.symbol
            else:
                self.dead = True
        else:
            self.arr[int(self.currentY)][int(self.currentX)] = " "
            
    

pygame.init()

width = 180
height = 40
array = createArr(width, height, " ")

thisPlayer = Particle(90, 30, "X", array)
thisMovement = MovementType.AUTO

powerups = []
powerUpTypes = ["A"]

lastRewardPowerUp = 0

lastUpdateScore = 0
i = 0

def doPowerUp(symbol): #UPDATE HERE TO ADD MORE POWER UPS
    if symbol == "A":
        thisPlayer.giveShots(5)
    if symbol == "S":
        global currentAttackerHorizontalSpeed
        global currentAttackerVerticalSpeed
        currentAttackerHorizontalSpeed = currentAttackerHorizontalSpeed * 0.5
        currentAttackerVerticalSpeed = currentAttackerVerticalSpeed * 0.5
    if symbol == "I":
        thisPlayer.invincible = True


def removePowerUps(): #UPDATE HERE TO ADD MORE POWER UPS
    global currentAttackerHorizontalSpeed
    global currentAttackerVerticalSpeed
    currentAttackerHorizontalSpeed = ATTACKER_HORIZONTAL_SPEED
    currentAttackerVerticalSpeed = ATTACKER_VERTICAL_SPEED
    thisPlayer.invincible = False

def useAndRemovePowerUp(x, y):
    for each in powerups:
        if each.X == x and each.Y == y:
            powerups.remove(each.useAndRemove())
    
    
while True:
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_q: #switches movement move (single to auto, auto to single)
                thisPlayer.dx = 0
                thisPlayer.dy = 0
                if thisMovement==MovementType.AUTO:
                    thisMovement = MovementType.SINGLE
                else:
                    thisMovement = MovementType.AUTO
            if event.key==pygame.K_SPACE:
                #thisPlayer.shootProjectile(thisPlayer.dx*0.25, thisPlayer.dy*0.25)
                randomNum = 1
            if event.key==pygame.K_w:
                thisPlayer.shootProjectile(0.0, -1.0)
            if event.key==pygame.K_s:
                thisPlayer.shootProjectile(0.0, 1.0)
            if event.key==pygame.K_a:
                thisPlayer.shootProjectile(-1.0, 0.0)
            if event.key==pygame.K_d:
                thisPlayer.shootProjectile(1.0, 0.0)
            if thisMovement==MovementType.AUTO:
                if event.key==pygame.K_UP:
                    thisPlayer.dy = -1
                if event.key==pygame.K_LEFT:
                    thisPlayer.dx = -2
                if event.key==pygame.K_RIGHT:
                    thisPlayer.dx = 2
                if event.key==pygame.K_DOWN:
                    thisPlayer.dy = 1
            elif thisMovement==MovementType.SINGLE:
                thisPlayer.arr[thisPlayer.currentY][thisPlayer.currentX] = " "
                if event.key==pygame.K_UP:
                    thisPlayer.currentY = (thisPlayer.currentY - 1) % len(thisPlayer.arr)
                if event.key==pygame.K_LEFT:
                    thisPlayer.currentX = (thisPlayer.currentX - 1) % len(thisPlayer.arr[0])
                if event.key==pygame.K_RIGHT:
                    thisPlayer.currentX = (thisPlayer.currentX + 1) % len(thisPlayer.arr[0])
                if event.key==pygame.K_DOWN:
                    thisPlayer.currentY = (thisPlayer.currentY + 1) % len(thisPlayer.arr)
        if event.type==pygame.KEYUP:
            if thisMovement==MovementType.AUTO:
                if event.key==pygame.K_UP:
                    thisPlayer.dy = 0
                if event.key==pygame.K_LEFT:
                    thisPlayer.dx = 0
                if event.key==pygame.K_DOWN:
                    thisPlayer.dy = 0
                if event.key==pygame.K_RIGHT:
                    thisPlayer.dx = 0

    thisPlayer.move(1)

    #Power Ups
    if i % (24000/(30 + thisPlayer.score)) == 0 or (thisPlayer.score % 20 == 0 and thisPlayer.score > lastRewardPowerUp):
        removePowerUps()
        if thisPlayer.score % 20 == 0:
            lastRewardPowerUp = thisPlayer.score
        while True:
            x = random.randint(0, len(array[0]) - 1)
            y = random.randint(0, len(array) - 1)

            if array[y][x] == " ":
                break
        
        powerups.append(PowerUp(x, y, powerUpTypes[random.randint(0, len(powerUpTypes)-1)], array))

    if thisPlayer.score == 15 and not powerUpTypes.__contains__("S"): #Enables S powerups at 15
        powerUpTypes.append("S")

    if thisPlayer.score == 50 and not powerUpTypes.__contains__("I"): # Enables I powerups at 50
        powerUpTypes.append("I")

    #UPDATE HERE TO ADD MORE POWER UPS


    if i % (5000/(50 + thisPlayer.score)) == 0:
        attackerArray.append(Attacker(random.randint(0, width), random.randint(0, int(height/2)), "O", thisPlayer, array))
        if thisPlayer.shotsLeft == 0:
            thisPlayer.giveShots(1)

    if (i + 1) % random.randint(1, 3000) == 0:
        centerX = random.randint(10, width - 10)
        centerY = random.randint(10, int(height/2) - 10)
        for x in range(random.randint(4, 12)):
            attackerArray.append(Attacker(random.randint(centerX-10, centerX+10), random.randint(centerY-10, centerY+10), "O", thisPlayer, array))

    for each in attackerArray:
        each.move()

    for each in powerups:
        each.show()

    if  thisPlayer.score > lastUpdateScore:
        ATTACKER_VERTICAL_SPEED = ATTACKER_VERTICAL_SPEED * 1.01
        currentAttackerVerticalSpeed = currentAttackerVerticalSpeed * 1.01
        ATTACKER_HORIZONTAL_SPEED = ATTACKER_HORIZONTAL_SPEED * 1.01
        currentAttackerHorizontalSpeed = currentAttackerHorizontalSpeed *1.01
        
        lastUpdateScore = thisPlayer.score


    os.system("clear")
    print("Shots Left: " + str(thisPlayer.shotsLeft))
    print(conCarArrayVert(array))
    print("Score: " + str(thisPlayer.score))
    print("Attacker Horizontal Speed: " + str(currentAttackerHorizontalSpeed) + " Attacker Vertical Speed: " + str(currentAttackerVerticalSpeed) + " Invincibility: " + str(thisPlayer.invincible))
    time.sleep(0.1)

    i += 1