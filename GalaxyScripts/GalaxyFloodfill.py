from PIL import Image
from itertools import product
import os 
import sys
import numpy as np
import math

##Node, or pixel point in the image "graph", used in the floodfill algorithm
class Node:
    def __init__(self,is_white,x,y):
        self.is_white = is_white
        self.x = x
        self.y = y


##Crops the image into 5x5 pixel matrices
def findCenter(im, tileSize):
    w,h = im.size   
    grid = product(range(0, h-h%tileSize, tileSize), range(0, w-w%tileSize, tileSize))  
    biggestAvgVal = 0
    for x, y in grid:   #divide the image into a collection of 5x5 pixel croppings
        box = (x, y, x+tileSize, y+tileSize)
        avg = findAvgRGB(im.crop(box))
        if(avg > biggestAvgVal):biggestAvgVal = avg
    grid2 = product(range(0, h-h%tileSize, tileSize), range(0, w-w%tileSize, tileSize))
    for x, y in grid2:  #Find the coordinates of the center
        box = (x, y, x+tileSize, y+tileSize)
        avg = findAvgRGB(im.crop(box))
        if(avg == biggestAvgVal):
            coord = (x,y)
            #print(avg)
            print("Center: " + str(coord))
            return coord
    return 0


##finds the average RGB value of a particular 5x5 pixel matrix
def findAvgRGB(box):
   pixelAvgList = []
   w,h = box.size
   for x in range(w):
       for y in range(h):
           r, g, b = box.getpixel((x,y))
           pixelAvgRGB = ((r*0.21) + (g*0.72) + (b*0.07))/3
           pixelAvgList.append(pixelAvgRGB)
   n = len(pixelAvgList)
   avgSum = 0
   for pixelAvgRGB in pixelAvgList:
       avgSum += pixelAvgRGB
   totalAvg = avgSum / n
   return totalAvg 


def convert_to_node(img,x,y):
    r,g,b = img.getpixel((x,y))
    if r == 255:
        is_white = True
    else:
        is_white = False
    point = Node(is_white,x,y)
    return point


##Floodfill algorithm converts the galaxy skeleton to black
def floodfill(image,x,y):
    cur_point = convert_to_node(image,x,y)

    Q = []
    Q.append(cur_point)

    while len(Q) != 0:
        n = Q.pop()
        north = convert_to_node(image,n.x,n.y+1)
        south = convert_to_node(image,n.x,n.y-1)
        east = convert_to_node(image,n.x+1,n.y)
        west = convert_to_node(image,n.x-1,n.y)
        if n.is_white == True:
            n.is_white = False
            image.putpixel((n.x,n.y),(0,0,0))
            #print(image.getpixel((n.x,n.y)))
            Q.append(west)
            Q.append(east)
            Q.append(north)
            Q.append(south)
    #image.show()
    return image

##Function that returns both the farthest point of a galaxy and the Euclidean Distance of that point
def getFarthestEuclidean(image,xCenter,yCenter):
    farthestDistance = 0
    farthestX = 0
    farthestY = 0
    w,h = image.size   
    euclideanDistance = 0
    for x in range(w):
        for y in range(h):
            r,g,b = image.getpixel((x,y))
            if r == 255:
                euclideanDistance = math.sqrt((x - xCenter)**2 + (y - yCenter)**2)
                if euclideanDistance > farthestDistance:
                    farthestX,farthestY = x,y
                    farthestDistance = euclideanDistance
    return farthestX,farthestY,farthestDistance

##Path to the original image folder, use your own directory
mypath = r"C:\Users\EddieBigPC\Desktop\GalaxyProject\OriginalGalaxyImageTesting"
dirs = os.listdir(mypath)
##Path to the skeletons being tested
path2 = r"C:\Users\EddieBigPC\Desktop\GalaxyProject\GalaxySkeletonTesting"
dirs2 = os.listdir(path2)

##For every original image
for file in dirs:
    imagePath = os.path.join(mypath, file)
    im = Image.open(imagePath)
    xCent,yCent = findCenter(im,5)                      ##Find the center of the original image galaxy                    
    print(xCent,yCent)                                     
    origImageName = os.path.basename(imagePath)         
    origImageName = origImageName.removesuffix('.jpg')
    
    for file in dirs2:                                  ##For every skeleton image
        imagePath2 = os.path.join(path2, file)
        skelImageName = os.path.basename(imagePath2)
        if origImageName in skelImageName:              ##If the skeleton image matches the original image
            im2 = Image.open(imagePath2)
            farX,farY,farD = getFarthestEuclidean(im2,xCent,yCent)      ##Get the Euclidean Distance of the farthest point in the galaxy                         
            print("X: " + str(farX) + " Y: " + str(farY)                
                 + " Euclidean Distance: " + str(farD))
            print(im2.getpixel((farX,farY)))
            im2 = floodfill(im2,xCent, yCent)                           ##Run the floodfill algorithm using the farthest point
            im2.save(imagePath2)
            #im2.show()







