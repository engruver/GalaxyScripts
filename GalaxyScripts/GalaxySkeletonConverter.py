##Script that converts the editted galaxy images to skeletons
from PIL import Image
import os, sys

def whiteOrBlack (im):
    newimdata = []
    whitecolor = (255,255,255)
    blackcolor = (0,0,0)
    for color in im.getdata():
        if color != whitecolor:
            newimdata.append( blackcolor )
        else:
            newimdata.append( whitecolor )
    newim = Image.new(im.mode,im.size)
    newim.putdata(newimdata)
    return newim

##WARNING All files in folder are converted to skeletons, do not use on original images
mypath = r"C:\Users\EddieBigPC\Desktop\GalaxyProject\GalaxySkeletonTesting"
dirs = os.listdir(mypath)
for file in dirs:
    imagePath = os.path.join(mypath, file)
    newImagePath = os.path.join(mypath, "(2)" + file )
    im = Image.open(imagePath)
    whiteOrBlack(im).save(newImagePath)


