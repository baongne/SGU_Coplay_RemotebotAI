from flask import Flask,render_template,Response,jsonify,request,session
from ultralytics import YOLO
import cv2
import math


app = Flask(__name__)

def video_detection(path_x):
    video_capture = path_x
    #Create a Webcam Object
    cap=cv2.VideoCapture(video_capture)
    frame_width=int(cap.get(3))
    frame_height=int(cap.get(4))
    #out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P','G'), 10, (frame_width, frame_height))

    # model=YOLO("modelAI1.pt")
    # classNames = ['3', 'go', 'hd1', 'hd2', 'hd3', 'hd4', 'hd5', 'stop', 'win']
    # classNames = ['-', '100RPM', '200RPM', '300RPM', 'CCW', 'CW','stop']  #model_- 13 september 2023 7_01.pt
    model=YOLO("modelAI5.pt")
    classNames = ['bunch', 'c', 'hd1', 'hi', 'hura', 'jutsu', 'like', 'love']  #modelAI3

    while True:
        success, img = cap.read()
        results=model(img,stream=True)
        for r in results:
            boxes=r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                print(x1,y1,x2,y2)
                cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
                conf=math.ceil((box.conf[0]*100))/100
                cls=int(box.cls[0])
                class_name=classNames[cls]
                label=f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                print(t_size)
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
        yield img
def generate_frames(path_x=''):
    yolo_output = video_detection(path_x)
    for detection in yolo_output:
        ref,buffer = cv2.imencode('.jpg',detection)
        frame= buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
@app.route('/video')
def video():
    #return Response(generate_frames(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames(path_x = 0),mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
    app.run(debug=True)