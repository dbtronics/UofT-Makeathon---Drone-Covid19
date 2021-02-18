# from gpiozero import LED
import cv2
import numpy as np

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)

# width and height of frame
w = 640
h = 480

# minimum value drone can rotate, in pixels moved from center
min_rotation = 100

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (w, h))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected people
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8), padding=(8,8) )

    max_weight = [-1.0]
    idx = 0

    # get box with highest ROI
    for i in range(len(weights)):
        if weights[i] > max_weight[0]:
            idx = i
            max_weight = weights[i]

    if(max_weight[0] >= 0.5):
        print (max_weight[0])
        xA, yA, xB, yB = boxes[i]

        if xA+0.5*xB < 0.5*w-min_rotation:
            print("Rotate counterclockwise")
        elif xA+0.5*xB > 0.5*w + min_rotation:
            print("Rotate clockwise")
    
        xB += xA
        yB += yA
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    #for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        #cv2.rectangle(frame, (xA, yA), (xB, yB),
           #               (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cv2.waitKey(1)
 
# led = LED(19)

# led.off()
 
detector = cv2.QRCodeDetector()
 
print("Reading QR code using Raspberry Pi camera")

data = ""
 
while data == "":
    # led.toggle()
    
    ret, img = cap.read()
    data, _, _ = detector.detectAndDecode(img)


print("Data found: " + data)
# led.on()

cap.release()