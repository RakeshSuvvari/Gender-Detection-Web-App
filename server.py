from flask import Flask, render_template, Response
from camera import VideoCamera
# Flask and camera.py imports

app = Flask(__name__)

video_camera = None
global_frame = None

@app.route('/')
def index():
    return render_template('index.html')


def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()
        
        #frame by frame check and yeilding
        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    #Host address to run on local machine
    app.run(host='0.0.0.0', threaded=True)