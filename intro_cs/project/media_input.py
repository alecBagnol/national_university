import cv2
picture = cv2.imread('pictures/futsal-barlev.jpg') 
# cv2.imshow('mario',picture)
# cv2.waitKey(0)

# print(len(picture[0][0]))

picture_b = picture
for row in range(len(picture_b)):
    for column in range(len(picture_b[row])):
        picture_b[row][column][0] = 255
        picture_b[row][column][1] = 255

cv2.imshow('mario blue',picture_b)
cv2.waitKey(0)


# capture = cv2.VideoCapture('pathvideo')
# while True:
#     isTrue, frame = capture.read()
#     cv2.imshow('video', frame)
#     if cv2.waitKey(20) & 0xFF==ord('d'):
#         break
# capture.release()
# cv2.destroyAllWindows()