import cv2
import numpy as np
import cv2 as cv
import imutils
import sys

DEFAULT_FILE_NAME = "imgg.png"
DEFAULT_SEARCH_TAMPLATE_FILE_NAME = "corner_template.png.png"

if len(sys.argv ) == 1:
    FLOOR_PLAN_LOCATION = "imgg.png"
    TEMPLATE_FILE_LOCATION = DEFAULT_SEARCH_TAMPLATE_FILE_NAME

elif len(sys.argv) == 2:
    TEMPLATE_FILE_LOCATION = DEFAULT_SEARCH_TAMPLATE_FILE_NAME
    FLOOR_PLAN_LOCATION = sys.argv[1]

elif len(sys.argv) == 3:
    TEMPLATE_FILE_LOCATION = sys.argv[2]
    FLOOR_PLAN_LOCATION = sys.argv[1]

ALL_ROTATIONS = 4 # set to 1 to show one corner (red), 0 for no corner detection, 4 for all corners
EDGE_DETECTION = 0 # 0 = None, 1 = Canny, 2 = Sobel edge detection
##################################################################


def contour_detection_method(img,imgc):
    """
    goes through all the findable conected contours in the image and colours them gold saves as contour.png

    :param img: the image in black and white after threshholding
    :param imgc: the image in colour for the contours to be overlaid onto
    :return: NA
    """
    contours = cv2.findContours(img.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    contours = imutils.grab_contours(contours)
    for c in contours[:-5]:
        cv2.drawContours(imgc,[c],-1,(0,200,255),2)

    cv2.imwrite("contour.png",imgc)

    ##uncomment to see the contour image

    # cv2.imshow("contour_image",imgc)

def run_edge_detection(img):
    """
    runs 2 edge detection methods Canny with treshhold 200,100 and sobel with kernal size 5
    :param img: the base image for edge detection
    :return: image after sobel edge detecttion, image after canney edge detection
    """

    Sobelx = cv.Sobel(src=img, ddepth=0, dx=1, dy=0, ksize=5)
    Sobely = cv.Sobel(src=img, ddepth=0, dx=0, dy=1, ksize=5)
    edgesx = cv2.add(Sobelx,Sobely)
    cv2.imwrite("SOBELs.png", edgesx)

    edgesc = cv2.Canny(img,200,100,edges = 50)
    cv2.imwrite("CANNY.png", edgesc)
    return edgesx,edgesc


if __name__ == '__main__':
    ## open the floor plan image twice once in greyscale then in (c)olour
    img = cv.imread(FLOOR_PLAN_LOCATION, 0)
    imgc = cv.imread(FLOOR_PLAN_LOCATION, 1)

    ## uncomment to see the floor plan
    # cv2.imshow("floorplan", img)


    edgesx,edgesc = run_edge_detection(img)


    ## SET VARIABLE ABOVE WITH DEFINITION FOR EDGE_DETECTION

    if EDGE_DETECTION == 0:
        img = img
    elif EDGE_DETECTION == 1:
        img = edgesc
    elif EDGE_DETECTION == 2:
        img = edgesx

    (thresh,black_and_white) = cv2.threshold(img,60,255,cv2.THRESH_BINARY)

    contour_detection_method(black_and_white.copy(),imgc.copy())

    ## i thought this would be easier to see then using an image in one of the other files you can also use a corner file if you uncomment the section bellow

    ## slow method for template generation
    corner_template =np.array( [
                                [0, 0,0,0, 0 ,0,0,0,0,0,0],
                                [0,0,255,255,255,255,255,255,255,255,255],
                                [0,0,255,255,255,255,255,255,255,255,255],
                                [0,0,255,255,255,255,255,255,255,255,255],
                                [0,0,255,255,255,255,255,255,255,255,255]])


    import time
    ## if you choose to use an image as corner_template uncomment the bellow

    # corner_template = cv.imread(str(TEMPLATE_FILE_LOCATION), 0)
    # (thresh,corner_template) = cv2.threshold(corner_template,110,255,cv2.THRESH_BINARY)

    ## un comment to see the sorner_template
    # cv2.imshow("corner_template", corner_template)



    cv2.imwrite(TEMPLATE_FILE_LOCATION,corner_template)
    corner_template = cv.imread(TEMPLATE_FILE_LOCATION, 0)



    ## needed for overlaying bounding boxs finds the width and hieght of corner kernal
    w,h = corner_template.shape[::-1]


    threshold = 0.8

    # defines the colours for each rotation of the corner kernal (see other documentation for orientation to colour table)
    outline_colours = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (175, 175, 175)]

    # sets default for rotate = 0
    rotate = 0


    ## SET VARIABLE ABOVE WITH DEFINITION FOR ALL ROTATIONS
    for rotate in range(0,ALL_ROTATIONS):
        res = cv.matchTemplate(img, corner_template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res > threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(imgc,pt,(pt[0]+w,pt[1]+h),outline_colours[rotate],2)
        corner_template = np.rot90(corner_template)




    ## if your wantingo see any image made use this format with imshow(filename, image)
    cv2.imshow("edgesc",imgc)

    ##holds runtime so images dont automatically close on end of programm
    cv2.waitKey(0)




