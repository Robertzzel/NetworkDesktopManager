import cv2 as cv
from Screen.screenshot import Screenshot

if __name__ == "__main__":

    img = Screenshot.get()
    cv.imshow('img', img)
    cv.waitKey()

    img = Screenshot.get()
    cv.imshow('img', img)
    cv.waitKey()