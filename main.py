import cv2
import mediapipe as mp
import math
import numpy as np
import comtypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Initialize COM
comtypes.CoInitialize()

# Volume control setup
devices = AudioUtilities.GetSpeakers()

interface = devices._dev.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Smooth volume variable
smoothVol = 0

while True:
    success, img = cap.read()

    if not success:
        break

    # Convert BGR to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process image
    results = hands.process(imgRGB)

    # Check if hand is detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            lmList = []

            # Get all landmark positions
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

            if len(lmList) != 0:
                # Thumb tip
                x1, y1 = lmList[4][1], lmList[4][2]

                # Index tip
                x2, y2 = lmList[8][1], lmList[8][2]

                # Draw circles
                cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)

                # Draw line
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

                # Calculate distance
                length = math.hypot(x2 - x1, y2 - y1)

                # Mute gesture
                if length < 25:
                    volume.SetMute(1, None)
                    cv2.putText(img, "MUTED", (200, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                else:
                    volume.SetMute(0, None)

                    # Map distance to volume
                    vol = np.interp(length, [20, 200], [minVol, maxVol])

                    # Smooth volume control
                    smoothVol = smoothVol + (vol - smoothVol) / 5
                    volume.SetMasterVolumeLevel(smoothVol, None)

                # Map distance to volume bar and percentage
                volBar = np.interp(length, [20, 200], [400, 150])
                volPer = np.interp(length, [20, 200], [0, 100])

                print("Distance:", length, "Volume:", smoothVol)

                # Draw volume bar
                cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

                # Display percentage
                cv2.putText(img, f'{int(volPer)} %', (40, 430),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            # Draw hand landmarks
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()