from tkinter import *

window = Tk()


def Keyboard():
    import cv2
    import mediapipe as freedomtech

    drawingModule = freedomtech.solutions.drawing_utils
    handsModule = freedomtech.solutions.hands

    mod = handsModule.Hands()

    h = 680
    w = 840

    def findpostion(frame):
        list = []
        results = mod.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                list = []
                for id, pt in enumerate(handLandmarks.landmark):
                    x = int(pt.x * w)
                    y = int(pt.y * h)
                    list.append([id, x, y])

        return list

    import cv2
    from pynput.keyboard import Controller
    from module import findpostion
    import math
    from time import sleep
    cap = cv2.VideoCapture(0)
    keyboard = Controller()
    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
    finalText = ""

    def draw(img, buttonlist):
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size
            cv2.rectangle(img, (button.pos), (x + w, y + h), (0, 0, 255), -1)
            cv2.putText(img, button.text, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        return img

    class button():
        def _init_(self, pos, text, size=[60, 60]):
            self.pos = pos
            self.text = text
            self.size = size

    buttonlist = []
    for i in range(3):
        for j, key in enumerate(keys[i]):
            buttonlist.append(button([70 * j + 20, 70 * i + 40], key))

    while True:

        ret, frame = cap.read()
        flipped = cv2.flip(frame, flipCode=1)
        frame = cv2.resize(flipped, (840, 680))

        a = findpostion(frame)
        frame = draw(frame, buttonlist)
        if len(a) != 0:
            for button in buttonlist:
                x, y = button.pos
                w, h = button.size
                x1, y1 = a[8][1], a[8][2]
                x2, y2 = a[12][1], a[12][2]
                length = math.hypot(x2 - x1, y2 - y1)
                if x < x1 < x + w and y < y1 < y + h:
                    cv2.rectangle(frame, (button.pos), (x + w, y + h), (122, 0, 122), -1)
                    cv2.putText(frame, button.text, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                    print(length)
                    if length < 30:
                        cv2.rectangle(frame, (button.pos), (x + w, y + h), (0, 255, 0), -1)
                        cv2.putText(frame, button.text, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                        finalText += button.text
                        keyboard.press(button.text)
                        keyboard.release(button.text)

        cv2.rectangle(frame, (50, 350), (700, 450), (122, 0, 122), -1)
        cv2.putText(frame, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        sleep(0.15)

        cv2.imshow("Frame", frame);
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def Paint():
    # All the imports go here
    import cv2
    import numpy as np
    import mediapipe as mp
    from collections import deque

    # Giving different arrays to handle colour points of different colour
    bpoints = [deque(maxlen=1024)]
    gpoints = [deque(maxlen=1024)]
    rpoints = [deque(maxlen=1024)]
    ypoints = [deque(maxlen=1024)]

    # These indexes will be used to mark the points in particular arrays of specific colour
    blue_index = 0
    green_index = 0
    red_index = 0
    yellow_index = 0

    # The kernel to be used for dilation purpose
    kernel = np.ones((5, 5), np.uint8)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    colorIndex = 0

    # Here is code for Canvas setup
    paintWindow = np.zeros((471, 636, 3)) + 255
    paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
    paintWindow = cv2.rectangle(paintWindow, (160, 1), (255, 65), (255, 0, 0), 2)
    paintWindow = cv2.rectangle(paintWindow, (275, 1), (370, 65), (0, 255, 0), 2)
    paintWindow = cv2.rectangle(paintWindow, (390, 1), (485, 65), (0, 0, 255), 2)
    paintWindow = cv2.rectangle(paintWindow, (505, 1), (600, 65), (0, 255, 255), 2)

    cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

    # initialize mediapipe
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    ret = True
    while ret:
        # Read each frame from the webcam
        ret, frame = cap.read()

        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
        frame = cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), 2)
        frame = cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), 2)
        frame = cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)
        frame = cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), 2)
        cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        # frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Get hand landmark prediction
        result = hands.process(framergb)

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # # print(id, lm)
                    # print(lm.x)
                    # print(lm.y)
                    lmx = int(lm.x * 640)
                    lmy = int(lm.y * 480)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
            fore_finger = (landmarks[8][0], landmarks[8][1])
            center = fore_finger
            thumb = (landmarks[4][0], landmarks[4][1])
            cv2.circle(frame, center, 3, (0, 255, 0), -1)
            print(center[1] - thumb[1])
            if (thumb[1] - center[1] < 30):
                bpoints.append(deque(maxlen=512))
                blue_index += 1
                gpoints.append(deque(maxlen=512))
                green_index += 1
                rpoints.append(deque(maxlen=512))
                red_index += 1
                ypoints.append(deque(maxlen=512))
                yellow_index += 1

            elif center[1] <= 65:
                if 40 <= center[0] <= 140:  # Clear Button
                    bpoints = [deque(maxlen=512)]
                    gpoints = [deque(maxlen=512)]
                    rpoints = [deque(maxlen=512)]
                    ypoints = [deque(maxlen=512)]

                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0

                    paintWindow[67:, :, :] = 255
                elif 160 <= center[0] <= 255:
                    colorIndex = 0  # Blue
                elif 275 <= center[0] <= 370:
                    colorIndex = 1  # Green
                elif 390 <= center[0] <= 485:
                    colorIndex = 2  # Red
                elif 505 <= center[0] <= 600:
                    colorIndex = 3  # Yellow
            else:
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(center)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(center)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(center)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(center)
        # Append the next deques when nothing is detected to avois messing up
        else:
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        # Draw lines of all the colors on the canvas and frame
        points = [bpoints, gpoints, rpoints, ypoints]
       
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

        cv2.imshow("Output", frame)
        cv2.imshow("Paint", paintWindow)

        if cv2.waitKey(1) == ord('q'):
            break

    # release the webcam and destroy all active windows
    cap.release()
    cv2.destroyAllWindows()


B1 = Button(window, text='Keyboard', command=Keyboard)
B2 = Button(window, text='Paint', command=Paint)
B1.pack()
B2.pack()
window.mainloop()