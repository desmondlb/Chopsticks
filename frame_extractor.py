import cv2

# cap = cv2.VideoCapture('WIN_20200807_14_38_46_Pro.mp4')
# cap = cv2.VideoCapture('WIN_20200807_14_39_17_Pro.mp4')
cap = cv2.VideoCapture('WIN_20200807_14_39_44_Pro.mp4')
i = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('NH3_' + str(i) + '.jpg', frame)
    i += 1

cap.release()
cv2.destroyAllWindows()