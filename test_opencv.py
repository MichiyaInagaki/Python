import cv2

img = cv2.imread('C:/image/lena.jpg')
print(img)
gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("C:/image/lena-gray.jpg", gry)

