# from flask import Flask, Response
# from flask_socketio import SocketIO, emit, send
# from ultralytics import YOLO
# import json
# import cv2

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# # @socketio.on('my event')
# # def handle_connect(data):
# #     print(data)

# @socketio.on('test event')
# def handle_testevent():
#     emit('test event', "{data:" + "Hello" + "}")

# def video_detection(path_x):
#     with app.app_context():
#         video_capture = path_x
#         cap = cv2.VideoCapture(video_capture)
#         model = YOLO("best.pt")
#         classNames = ["go", "stop"]
#         while True:
#             success, img = cap.read()
#             results = model(img, stream=True)
#             for r in results:
#                 boxes = r.boxes
#                 for box in boxes:
#                     class_name = classNames[int(box.cls[0])]
#                     socketio.emit("test event", {'data': class_name})
                    
#             yield img

# def generate_frames(path_x=''):
#     yolo_output = video_detection(path_x)
#     for detection in yolo_output:
#         ref, buffer = cv2.imencode('.jpg', detection)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video')
# def video():
#     return Response(generate_frames(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     socketio.run(app, debug=True, allow_unsafe_werkzeug=True)




from flask import Flask, Response
from flask_socketio import SocketIO, emit, send
from ultralytics import YOLO
import json
import cv2
import math

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# @socketio.on('my event')
# def handle_connect(data):
#     print(data)

@socketio.on('test event')
def handle_testevent():
    emit('test event', "{data:" + "Hello" + "}")

def video_detection(path_x):
    with app.app_context():
        video_capture = path_x
        
        cap = cv2.VideoCapture(video_capture)
        model=YOLO("modelAI7.pt")
        classNames = ['bunch', 'c', 'hd1', 'hi', 'hura', 'jutsu', 'like', 'love']  #modelAI3
        
        while True:
            _, img = cap.read()
            results = model.predict(img, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes :
                    x1,y1,x2,y2=box.xyxy[0]
                    x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                    print(x1,y1,x2,y2)
                    cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
                    conf=math.ceil((box.conf[0]*100))/100
                    cls=int(box.cls[0])
                    class_name=classNames[cls]                   
                    socketio.emit("test event", {'data': class_name})
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
        ref, buffer = cv2.imencode('.jpg', detection)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)



#hello