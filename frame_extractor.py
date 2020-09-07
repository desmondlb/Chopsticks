import cv2

# cap = cv2.VideoCapture('WIN_20200807_14_38_46_Pro.mp4')
# cap = cv2.VideoCapture('WIN_20200807_14_39_17_Pro.mp4')
cap = cv2.VideoCapture('D:/Projects/Chopsticks/Datasets/4/WIN_20200825_18_56_00_Pro.mp4')
i = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('D:/Projects/Chopsticks/Datasets/4/fourr_' + str(i) + '.jpg', frame)
    i += 1

cap.release()
cv2.destroyAllWindows()