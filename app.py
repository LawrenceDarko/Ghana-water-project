import cv2
import numpy
from flask import Flask, render_template, Response, stream_with_context, request
import RPi.GPIO as GPIO
import time
trigPin = 23
echoPin = 24

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(trigPin,GPIO.OUT)
	GPIO.setup(echoPin,GPIO.IN)

def distance():
    setup()
    GPIO.output(trigPin ,0)
    time.sleep(2E-6)
    GPIO.output(trigPin , 1)
    time.sleep(10E-6)
    GPIO.output(trigPin,0)
    
    while GPIO.input(echoPin)==0:
        pass
    echoStartTime =time.time()
    while GPIO.input(echoPin)==1:
        pass
    echoStopTime = time.time()
    
    pingTravelTime = echoStopTime - echoStartTime
    pingTravelTime = (int(pingTravelTime*1E6))
    pingTravelDistance = (pingTravelTime*765.*5280.*12)/(3600.*1000000)
    pingDistanceToTarget = pingTravelDistance/2.
    pingDistanceToTarget = pingDistanceToTarget/39.37
    pingDistanceToTarget = "{:.1f}".format(pingDistanceToTarget)
    
    return float(pingDistanceToTarget)
#     return 5.0 - float(pingDistanceToTarget


video = cv2.VideoCapture(0)
app = Flask('__name__')


def video_stream():
    while True:
        ret, frame = video.read()
        if not ret:
            break;
        else:
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')


@app.route('/')
@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/get_distance")
def get_distance():
    try:
        dist = distance()
#         dist = 123
        print(dist," meters(m)")
        return "Water height = " + str(dist) +" meters(m)"
    except KeyboardInterrupt():
        GPIO.cleanup()
        print("ERROR")
# 	return "hello " +" meters(m)"

@app.route("/get_distance2")
def get_distance2():
	return " Hello " + "21 meters(m)"


if __name__ == "__main__":
    app.run()
#    app.run(host='0.0.0.0', port='5000', debug=False)
    app.run(hostname='0.0.0.0')
 	
	
	
