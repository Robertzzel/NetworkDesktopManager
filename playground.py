import cv2

if __name__ == "__main__":
    cursor_image = cv2.imread("Images/cursor.png", cv2.IMREAD_GRAYSCALE)
    cv2.imshow("cursor", cursor_image)
    cv2.waitKey()