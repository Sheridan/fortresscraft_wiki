import os
import itertools as it
import numpy as np
import cv2

## Args
FilePath = 'gui.png'
OutImageFolder = 'Sprites'


## Load image and add white border
imgInput = cv2.imread(FilePath, cv2.IMREAD_UNCHANGED)
#imgInput = cv2.cvtColor(imgInput, cv2.COLOR_BGRA2RGBA)
imgInput = cv2.copyMakeBorder(imgInput, 10, 10, 10, 10,cv2.BORDER_CONSTANT,value = [0, 0, 0, 0])

## Convert image to gray
imgGray = cv2.cvtColor(imgInput, cv2.COLOR_BGRA2GRAY)
#cv2.imwrite('gui Gray.png', imgGray)

## Apply threshold
thMin = 1
_, imgTh = cv2.threshold(imgGray, thMin, 255, cv2.THRESH_BINARY)
#cv2.imwrite('gui Threshold.png', imgTh)

## Find Contourns
cntsMinArea = 100

cnts, hierarchy = cv2.findContours(imgTh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#cnts = list(it.compress(cnts, (hierarchy[:, :, 3] == 0)[0])) ## Keep only the ones that have the root as parent
cnts = filter(lambda x: cv2.contourArea(x) > cntsMinArea, cnts) ## Remove the small ones
cnts = sorted(cnts, key = lambda x: cv2.contourArea(x), reverse = True) ## Sort by area

## Draw Contourns
imgCnts = imgInput.copy()
cv2.drawContours(imgCnts, cnts, -1, (255,0,128, 255), 2)
#cv2.imwrite('gui Contourns.png', imgCnts)

## Extract contours images
fileOutFormat = os.path.join(OutImageFolder, '{0}.png')
imgBlank = np.zeros_like(imgInput)
cntsLen = len(cnts)

for i, cnt in enumerate(cnts):
    print 'Extracting sprite {0}/{1}'.format(i+1, cntsLen)

    ## Create contour mask
    mask = cv2.cvtColor(imgBlank.copy(), cv2.COLOR_BGRA2GRAY)
    cv2.drawContours(mask, cnts, i, 255, -1)

    ## Apply mask to Input Img
    imgCnt = imgBlank.copy()
    imgCnt[mask == 255] = imgInput[mask == 255]

    ## Extract bounding rect of the crop
    bRect = cv2.boundingRect(cnt)

    ## Crops contours
    x, y, w, h = bRect
    imgCntCropped = imgCnt[y:y+h, x:x+w]

    ## Sava image to file
    cv2.imwrite(fileOutFormat.format(i), imgCntCropped)

