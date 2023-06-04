import cv2
import numpy as np
import random
import math

random.seed()

width = 1280
height = 720
evolutionRate = 5.0
numPoints = 4
multiplier = 5

distY = np.transpose(np.tile(np.linspace(-height, height, height * 2), (width * 2, 1)))
distX = np.tile(np.linspace(-width, width, width * 2), (height * 2, 1))
frame = np.empty([height, width, 3])

currDistY = np.power(distY, 2)
currDistX = np.power(distX, 2)
distMat = np.sqrt(currDistY + currDistX)

def draw(points):
    sumDist = np.zeros((height, width))

    frame[:,:,:] = 0
    for n in range(0, len(points)):
        y1 = math.floor(points[n].pos[0])
        y2 = math.floor(y1 + height)
        x1 = math.floor(points[n].pos[1])
        x2 = math.floor(x1 + width)
        sumDist += distMat[y1:y2,x1:x2]
        for dim in range(0, 3):
            frame[:,:,dim] += points[n].color[dim] * distMat[y1:y2,x1:x2]

    for dim in range(0, 3):
        frame[:,:,dim] = (frame[:,:,dim] / sumDist) * multiplier % 1.0

    return frame

class Point:

    def __init__(self):
        self.pos = [random.randint(0, height), random.randint(0, width)]
        self.color = [random.random(), random.random(), random.random()]
        self.direction = random.random() * 2 * math.pi
        self.speed = [random.random() * evolutionRate, random.random() * evolutionRate]
        self.currPos = []

    def step(self):
        self.pos = [
            self.pos[0] + self.speed[0],
            self.pos[1] + self.speed[1]
        ]

        # keep point coordinates in the frame
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.speed[0] *= -1.0
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.speed[1] *= -1.0
        if self.pos[0] > height:
            self.pos[0] = height
            self.speed[0] *= -1.0
        if self.pos[1] > width:
            self.pos[1] = width
            self.speed[1] *= -1.0

points = []
for i in range(0, numPoints):
    points.append(Point())

seconds = 60
fps = 30

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))


num_frames = seconds * fps
print("Generating %d frames" % num_frames)
for index in range(num_frames):
    print(index)
    for point in points:
        point.step()

    frame = draw(points)
    
    # Write the frame into the file 'output.mp4'
    out.write(np.uint8(frame*255))
