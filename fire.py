import time, sys, select, os, pygame, random, time
from enum import Enum

STARTING_SHOTS = 20
JUMP_RADIUS = 1.5
SHOTS_FOR_KILL = 1
ATTACKER_VERTICAL_SPEED = 0.5
ATTACKER_HORIZONTAL_SPEED = 1.0

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


class Particle(object):

    currentX = 0
    currentY = 0
    symbol = "X"
    arr = []

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
            if self.arr[int(self.currentY)][int(self.currentX)] == "O" and depth == 1:
                os._exit(0)
            if self.arr[int(self.currentY)][int(self.currentX)] == "O" and depth == 0:
                for each in findAttackers(int(self.currentY), int(self.currentX)):
                    each.die()

            self.arr[int(self.currentY)][int(self.currentX)] = " "

            if depth == 1: # Player Case
                self.currentY = (self.currentY + self.dy) % len(self.arr)
                self.currentX = (self.currentX + self.dx) % len(self.arr[0])
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
            elif self.arr[int(self.currentY)][int(self.currentX)] == "X": # Kills player
                os._exit(0)

            distance = ((self.currentX - self.target.currentX)**2 + (self.currentY - self.target.currentY)**2)**0.5

            if distance > JUMP_RADIUS: # Moves
                self.dx = ATTACKER_HORIZONTAL_SPEED*(self.target.currentX - self.currentX)/distance
                self.dy = ATTACKER_VERTICAL_SPEED*(self.target.currentY - self.currentY)/distance

                self.currentY = (self.currentY + self.dy)
                if random.random() < 0.4:
                    self.currentY += + (random.random()*2 - 1)*ATTACKER_VERTICAL_SPEED
                self.currentX = (self.currentX + self.dx)
                if random.random() < 0.4:
                    self.currentX += + (random.random()*2 - 1)*ATTACKER_HORIZONTAL_SPEED
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

lastUpdateScore = 0
i = 0
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
                    thisPlayer.dx = -1
                if event.key==pygame.K_RIGHT:
                    thisPlayer.dx = 1
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

    if i % (5000/(50 + thisPlayer.score)) == 0:
        attackerArray.append(Attacker(random.randint(0, width), random.randint(0, height/2), "O", thisPlayer, array))
        if thisPlayer.shotsLeft == 0:
            thisPlayer.giveShots(1)

    if (i + 1) % random.randint(1, 3000) == 0:
        centerX = random.randint(10, width - 10)
        centerY = random.randint(10, height/2 - 10)
        for x in xrange(random.randint(4, 12)):
            attackerArray.append(Attacker(random.randint(centerX-10, centerX+10), random.randint(centerY-10, centerY+10), "O", thisPlayer, array))

    for each in attackerArray:
        each.move()

    if  thisPlayer.score > lastUpdateScore:
        ATTACKER_VERTICAL_SPEED = ATTACKER_VERTICAL_SPEED * 1.01
        ATTACKER_HORIZONTAL_SPEED = ATTACKER_HORIZONTAL_SPEED * 1.01
        
        lastUpdateScore = thisPlayer.score


    os.system("clear")
    print("Shots Left: " + str(thisPlayer.shotsLeft))
    print(conCarArrayVert(array))
    print("Score: " + str(thisPlayer.score))
    time.sleep(0.03)

    i += 1