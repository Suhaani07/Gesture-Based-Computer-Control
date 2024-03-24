import cv2
import screen_brightness_control as sbc
import numpy as np

face_classifier=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_classifier=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

video_capture=cv2.VideoCapture(0)
brightness =sbc.get_brightness()
while True:
    result,vid=video_capture.read()
    if result is False:
        break

    gray_image=cv2.cvtColor(vid,cv2.COLOR_BGR2GRAY)

    face=face_classifier.detectMultiScale(gray_image,1.1,4,minSize=(200,200))
    for (x,y,w,h) in face:
        cv2.rectangle(vid,(x,y),(x+w,y+h),(255,0,0),2)

        boundary=gray_image[y:y+h,x:x+w]
        boundary_color=vid[y:y+h,x:x+w]
        eyes=eye_classifier.detectMultiScale(boundary,1.1,4,minSize=(70,70))

    if(len(eyes)>=2):
        eye1x,eye1y,eye1w,eye1h=eyes[0]
        eye2x,eye2y,eye2w,eye2h=eyes[1]

        eye1_centre=(int(eye1x+eye1w/2),int(eye1y+eye1h/2))
        eye2_centre=(int(eye2x+eye2w/2),int(eye2y+eye2h/2))

        cv2.circle(boundary_color,eye1_centre,2,(0,0,255),2)
        cv2.circle(boundary_color,eye2_centre,2,(0,0,255),2)
        cv2.line(boundary_color,eye1_centre,eye2_centre,(0,0,255),2)

        x=(eye2_centre[0]-eye1_centre[0])
        y=(eye2_centre[1]-eye1_centre[1])

        angle = np.arctan2(y, x) * 180 / np.pi
       
        if(angle>30):
            sbc.set_brightness(int(brightness[0])-50)
            cv2.putText(vid, "Decreased Brightness", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        elif(angle<-30):
            sbc.set_brightness(int(brightness[0])+50)
            cv2.putText(vid, "Increased Brightness", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
   
    cv2.imshow("Detected Face and eyes",vid)

    if cv2.waitKey(1) == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()