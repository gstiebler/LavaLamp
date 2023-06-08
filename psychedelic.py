# Importing necessary modules
# cv2 for image manipulation, numpy for numerical operations, random for generating random numbers and math for mathematical functions.
import cv2
import numpy as np
import random
import math

# Setting the seed for random number generator, ensuring that the random numbers are reproducible.
random.seed()

# Defining the width and height of the output frame
width = 1280
height = 720

# Evolution rate defines the speed at which the points will move
evolutionRate = 5.0

# Number of points that will be generated
numPoints = 4

# The factor by which the distance from each pixel to the point influences the final color of the pixel
multiplier = 5

# Creating matrices that hold the distance of each pixel to the origin (0,0)
# We need both horizontal and vertical distances. distX and distY are 2D arrays that represent these distances.
distY = np.transpose(np.tile(np.linspace(-height, height, height * 2), (width * 2, 1)))
distX = np.tile(np.linspace(-width, width, width * 2), (height * 2, 1))

# Initializing an empty frame with 3 color channels (Red, Green, Blue)
frame = np.empty([height, width, 3])

# Calculating the distance of each pixel to the origin using the Pythagorean theorem
currDistY = np.power(distY, 2)
currDistX = np.power(distX, 2)
distMat = np.sqrt(currDistY + currDistX)

# This function calculates the colors for each pixel based on the distances to the points
def draw(points):
    sumDist = np.zeros((height, width))

    # Clearing the frame at the beginning
    frame[:,:,:] = 0

    # Calculating the sum of distances for each pixel to each point
    for n in range(0, len(points)):
        # Selecting a region of the frame that's as large as the current point's distance matrix
        y1 = math.floor(points[n].pos[0])
        y2 = math.floor(y1 + height)
        x1 = math.floor(points[n].pos[1])
        x2 = math.floor(x1 + width)

        # Adding up the distances from each pixel to each point
        sumDist += distMat[y1:y2,x1:x2]

        # Calculating the color contribution of the current point for each pixel and adding it to the frame
        for dim in range(0, 3):
            frame[:,:,dim] += points[n].color[dim] * distMat[y1:y2,x1:x2]

    # Normalizing the color values and applying the multiplier
    for dim in range(0, 3):
        frame[:,:,dim] = (frame[:,:,dim] / sumDist) * multiplier % 1.0

    # Returning the final colored frame
    return frame

# Class definition for Point, which contains its position, color, direction, speed and current position
class Point:

    # Initialize the point with random position, color, direction and speed
    def __init__(self):
        self.pos = [random.randint(0, height), random.randint(0, width)]
        self.color = [random.random(), random.random(), random.random()]
        self.direction = random.random() * 2 * math.pi
        self.speed = [random.random() * evolutionRate, random.random() * evolutionRate]
        self.currPos = []

    # This function updates the position of the point based on its speed, also making sure it doesn't leave the frame
    def step(self):
        self.pos = [
            self.pos[0] + self.speed[0],
            self.pos[1] + self.speed[1]
        ]

        # If the point hits a border of the frame, it "bounces" back, reversing its speed in that dimension
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

# Initialize points
points = []
for i in range(0, numPoints):
    points.append(Point())

# The simulation is going to run for this many seconds
seconds = 60

# Frames per second of the output video
fps = 30

# Define the codec using VideoWriter_fourcc() and create a VideoWriter object
# 'mp4v' is a codec that is compatible with .mp4 format. 
# Note: '*' in front of 'mp4v' is used to unpack the string into four individual characters.
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Initialize the VideoWriter object where 'output.mp4' is the output filename, 
# fourcc defines the codec, fps is the frame rate and (width, height) is the frame size.
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

# Calculate the total number of frames
num_frames = seconds * fps

print("Generating %d frames" % num_frames)

# Start of the main loop that generates the frames
for index in range(num_frames):

    # Display the current frame index
    print(index)

    # Move each point for each frame
    for point in points:
        point.step()

    # Draw the current frame
    frame = draw(points)

    # Write the frame into the file 'output.mp4'
    # The frame needs to be converted to 8-bit unsigned integer format, and values need to be scaled to 0-255 range 
    # because OpenCV expects colors in this format.
    out.write(np.uint8(frame*255))

# At the end of the program, the VideoWriter object needs to be released.
# It is a good practice to release resources when they are no longer needed.
out.release()

