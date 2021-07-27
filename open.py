import cv2
import numpy as np
from time import sleep

largura_min = 100
altura_min = 100

offset = 6

pos = 550

delay = 60

detection = []
count = 0


def center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


cap = cv2.VideoCapture('sample_videos/video.mp4')
subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
    ret, frame1 = cap.read()
    tempo = float(1 / delay)
    sleep(tempo)
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = subtractor.apply(blur)
    diattte = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.morphologyEx(diattte, cv2.MORPH_CLOSE, kernel)
    x = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    contour, h = cv2.findContours(x, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1, (0, pos), (600, pos), (255, 127, 0), 3)
    for (i, c) in enumerate(contour):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_contour = (w >= largura_min) and (h >= altura_min)
        if not validate_contour:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        mid = center(x, y, w, h)
        detection.append(mid)
        cv2.circle(frame1, mid, 4, (0, 0, 255), -1)

        for (x, y) in detection:
            if y < (pos + offset) and y > (pos - offset):
                count += 1
                cv2.line(frame1, (25, pos), (1200, pos), (0, 127, 255), 3)
                detection.remove((x, y))
                print("car is detected : " + str(count))

    cv2.putText(frame1, "VEHICLE COUNT : " + str(count), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("Video Original", frame1)
    #cv2.imshow("Detectar", dilatada)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()
