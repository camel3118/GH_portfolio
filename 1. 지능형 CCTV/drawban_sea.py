import numpy as np
import cv2
import mysql.connector
import pafy
def main():
    #cap = cv2.VideoCapture(https://www.youtube.com/watch?v=wYPkDMVoxWo)  # Open video file
    url = 'https://www.youtube.com/watch?v=wYPkDMVoxWo'
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(best.url)
    conn = mysql.connector.connect(host="127.0.0.1",user="root",password="1234",database="loitering_log2")
    cursor = conn.cursor()
    
    cctvid = input('CCTV ID : ')
    info = input('invasion / loitering : ')
    
    polygon = []
    points = []
    
    while (cap.isOpened()):
        ret, frame = cap.read()  # read a frame
        if not ret:
            print('EOF')
            break

        frame = cv2.polylines(frame, polygon, True, (255, 0, 0), thickness=5)

        cv2.imshow('Frame', frame)
        # Abort and exit with 'Q'
        key = cv2.waitKey(25)
        if (key == ord('q')):
            break
        elif (key== ord('p')): 
            polygon = [np.int32(points)]
            #points = []

        cv2.setMouseCallback('Frame', left_click_detect, points)
        
    sql = "INSERT INTO cctv_info_sea VALUES (%s, %s, %s)"
    val = (cctvid, info, str(points))
    cursor.execute(sql,val)
    conn.commit()  
    cursor.close()
    conn.close()

    cap.release()  # release video file
    cv2.destroyAllWindows()  # close all openCV windows
    
def left_click_detect(event, x, y, flags, points):
    if (event == cv2.EVENT_LBUTTONDOWN):
        print(f"\tClick on {x}, {y}")
        points.append([x,y])
        print(points)
                       
main()
