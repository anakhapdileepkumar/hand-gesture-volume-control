import cv2

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    if not success:
        print("Camera not working")
        break

    cv2.imshow("Webcam Feed", img)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()