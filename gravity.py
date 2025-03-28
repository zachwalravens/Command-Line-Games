import time, sys, select, os, pygame, random, time

GRAVITY = 1

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

class Particle(object):

    x = 0
    y = 0
    xVelocity = 0
    yVelocity = 0
    arr = []
    height = 0

    lastX = x
    lastY = y

    def __init__(self, x, y, xVelocity, yVelocity, arr):
        self.x = x
        self.y = y
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.arr = arr
        self.height = len(self.arr)

    def update(self):
        if self.arr[self.lastY][self.lastX] != "O":
            self.arr[self.lastY][self.lastX] = " "

        self.x = (self.x + self.xVelocity) % len(self.arr[0])
        self.y += self.yVelocity
        if self.y > self.height:
            #self.yVelocity = -1*self.yVelocity
            #self.y = self.height - (self.y - self.height)
            os._exit(0)
        if self.y < 0:
            os._exit(0)
        self.yVelocity += GRAVITY*0.1

        if self.arr[int(self.y)][int(self.x)] != "O":
            self.arr[int(self.y)][int(self.x)] = "X"
        self.lastX = int(self.x)
        self.lastY = int(self.y)

        self.checkForIntersection()

    def checkForIntersection(self):
        if self.arr[int(self.y)][int(self.x)] == "O":
            os._exit(0)

class Blocker(object):

    startX = 40
    arr = []
    width = 3
    gapSize = 5
    gapY = 10

    def __init__(self, startX, gapSize, gapY, arr):
        self.arr = arr
        self.gapSize = gapSize
        self.gapY = gapY
        self.startX = startX

    def doShit(self):
        if self.startX >= -1 and self.startX < len(array[0]) - 1:
            for y in range(len(self.arr)):
                if y < self.gapY or y >= self.gapY + self.gapSize:
                    self.arr[y][self.startX + 1] = " "
                    if self.startX >= 0:
                        self.arr[y][self.startX] = "O"
        self.startX += -1

width = 150
height = 40

array = createArr(width, height, " ")
pygame.init()

thisParticle = Particle(40, 10, 0, 0, array)
blockerArray = []
nextBlockerStartX = 60

for x in range(30):
    blockerArray.append(Blocker(nextBlockerStartX, random.randint(7, 10), random.randint(5, 25), array))
    nextBlockerStartX += 40

score = 0
i = 0
while True:
    for event in pygame.event.get():
        if event.type in (pygame.KEYDOWN, pygame.KEYUP) and event.key == pygame.K_UP:
            thisParticle.yVelocity = -1.0


    thisParticle.update()

    if (i + 39) % 80 == 0:
        score += 1


    if i % 2 == 0:
        for each in blockerArray:
            each.doShit()


    os.system("clear")
    print(conCarArrayVert(array))
    print("Score: " + str(score))
    time.sleep(0.02)

    i += 1
