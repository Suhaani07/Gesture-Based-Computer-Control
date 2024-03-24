import cv2
import mediapipe as mediapipe
import pyautogui

cap = cv2.VideoCapture(0)
screen_width,screen_height=pyautogui.size()
pyautogui.SLOWMOUSE = True
cap.set(3,screen_width)
cap.set(4,screen_height)
hand_detector=mediapipe.solutions.hands.Hands()
drawing_utils=mediapipe.solutions.drawing_utils

while True:
    _,frame=cap.read()
    frame=cv2.flip(frame,1)
    frame_height,frame_width,_=frame.shape
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    output=hand_detector.process(rgb_frame)
    hands=output.multi_hand_landmarks
    index_y=0
    key = cv2.waitKey(1) & 0xFF
    if hands:
        for hand in hands:
           drawing_utils.draw_landmarks(frame,hand,mediapipe.solutions.hands.HAND_CONNECTIONS)
           allmarks=hand.landmark
           for id,lm in enumerate(allmarks):
               x,y=int(lm.x*frame_width),int(lm.y*frame_height)
               if id==8:
                   cv2.circle(img=frame,center=(x,y),radius=10,color=(255,0,0))
                   index_x,index_y=screen_width/frame_width*x,screen_height/frame_height*y
                   pyautogui.moveTo(index_x,index_y)
               if id==12:
                   cv2.circle(img=frame,center=(x,y),radius=10,color=(255,0,0))
                   thumb_x,thumb_y=screen_width/frame_width*x,screen_height/frame_height*y
                   print(abs(index_y-thumb_y))
                   if abs(index_y-thumb_y)<10:
                          pyautogui.click()
                          pyautogui.sleep(1)
    cv2.imshow("Mouse",frame)
    if key == ord("q"):
        break