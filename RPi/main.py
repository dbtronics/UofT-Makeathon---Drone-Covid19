from gpiozero import LED
import cv2
import re
 
led = LED(19)

led.on()
 
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
 
print("Reading QR code using Raspberry Pi camera")

data = ""
 
while data != "":
    led.toggle()
    
    _, img = cap.read()
    data, _, _ = detector.detectAndDecode(img)

if data:
    print("Data found: " + data)
    led.off()
 
led.off()
cap.release()
cv2.destroyAllWindows()