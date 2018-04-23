import cv2
import numpy as np
image = cv2.imread('rouge.jpg')
def filter1 (image) :
    height, width = image.shape[:2]
    for y in range (height) :
        for x in range (width) :
            pixel = image[y,x]
            for z in range (len(pixel)) :
                pixel [z] = (0.4*pixel[0]+4*pixel[1]+1.2*pixel[2])/4
            image[y,x] = pixel
    return image
def grey_filter_progressive (image) :
    height, width = image.shape[:2]
    coeff = 1
    for y in range (width) :
        for x in range (height) :
            pixel = image[x,y]
            for z in range (len(pixel)) :
                pixel [z] = (0.299*pixel[0]+0.587*pixel[1]+0.114*pixel[2])*(-coeff+1)+pixel[z]*coeff
            image[x,y] = pixel
        coeff = coeff-(1/width)
    return image
def grey_filter (image) :
    height, width = image.shape[:2]
    for y in range (width) :
        for x in range (height) :
            pixel = image[x,y]
            for z in range (len(pixel)) :
                pixel [z] = 0.299*pixel[0]+0.587*pixel[1]+0.114*pixel[2]
            image[x,y] = pixel
    return image
def revert_filter (image) :
    height, width = image.shape[:2]
    for y in range (width) :
        for x in range (height) :
            temp = image [x,y]
            image [x,y] = image [-x,-y]
            image[-x,-y] = temp
    return image
temp = image
cv2.imshow('image',filter1(temp))
cv2.waitKey(0)
cv2.destroyAllWindows()
