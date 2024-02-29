import cv2
from HandTrackingModule import handDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
import HandTrackingModule as htm
import time
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

folderPath = "fingers" # name of the folder, where there are images of fingers
fingerList = os.listdir(folderPath) # list of image titles in 'fingers' folder
overlayList = []
for imgPath in fingerList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)
totalFingers = 0

detector = handDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["<", " "]]
finalText = ""
keyboard = Controller()

def drawALL(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(imgNew, (x, y, w, h), 20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha, 0)[mask]
    return out

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img, draw=False)

    img = drawALL(img, buttonList)

    lmList, bboxInfo = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingers = detector.fingersUp()
        if lmList[4][1] < lmList[20][1]:
            totalFingers = fingers.count(1)
        else:
            totalFingers = fingers.count(1) - 1 if fingers[0] == 1 else fingers.count(1)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ =  detector.findDistance(8, 12, img, draw=False)

                ## when clicked
                if l < 30:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    if button.text == "<":
                        finalText = finalText[:-1]
                        keyboard.press('\010')
                    else:
                        finalText += button.text
                        keyboard.press(button.text)
                    sleep(0.15)

    cv2.rectangle(img, (50, 710), (700, 610), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 690), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    
    if lmList:
        fingersUp = detector.fingersUp()
        totalFingers = fingersUp.count(1)

    h, w, c = overlayList[totalFingers].shape

# Розміри зображення
    img_height, img_width = img.shape[:2]

# Розміри зображення перекладеного imageN
    image_height, image_width = overlayList[totalFingers].shape[:2]

# Координати для відображення image в правому нижньому куті
    x_offset = img_width - image_width
    y_offset = img_height - image_height
 
# Копіювання зображення в правий нижній кут
    img[img_height - image_height:img_height, img_width - image_width:img_width] = overlayList[totalFingers]

    cTime = time.time()
    fps = 1/ (cTime-pTime)
    pTime = cTime

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    # Змінені координати та розміри для відображення елементів в іншому боці та зменшення їх розміру
    cv2.putText(img, f'FPS: {int(fps)}', (img.shape[1] - 300, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 1)
    cv2.rectangle(img, (img.shape[1] - 100, 25), (img.shape[1] - 50, 60), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(totalFingers), (img.shape[1] - 90, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)   