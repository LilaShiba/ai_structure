from flask import Flask, render_template, Response, request
# in dev
#from agent.eyes import Eyes
import time
import os
import RPi.GPIO as GPIO
from picamera import PiCamera



app = Flask(__name__)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

PIR_PIN = 26
IR_LED_PIN = 17  
SERVO_PIN = 18
SWITCH_PIN = 16
# Set GPIO pins 
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(IR_LED_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Eyes()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    img = request.form['img']
    filename = 'static/images/' + str(int(time.time())) + '.jpg'
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(img))
    return filename

#TODO FIX Stream to be live
@app.route('/stream')
def stream():
    return Response(get_sensor_data())

# Motion Sensor
@app.route('/pir')
def pir():
    if GPIO.input(PIR_PIN):
        data = {'status': 'Motion detected'}
    else:
        data = {'status': 'No motion'}
    return render_template('pir.html', data=data)

# IR Blaster
@app.route('/ir')
def ir():
   # while True:
        # Send the IR signal for the selected device
    for device, value in off_signals.items():
        send_ir_signal(off_signals[device])
        time.sleep(1)  # Wait for 1 second before sending another signal
    cycle = {'status': 'complete'}
    return render_template('ir.html',data=cycle)
    
@app.route('/kiki')
def kiki():
    pass

# helpers
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# if rpi
def gen():
    camera.start_preview()
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def intuition():
    # TODO refactor atoms - tissue
    pass

def generate_pir_data():
    #GPIO.setmode(GPIO.BCM)
    # TODO: Make Dynamic
    sensor_pin = PIR_PIN
    GPIO.setup(sensor_pin, GPIO.IN)

    while True:
        pir_state = GPIO.input(PIR_PIN)
        yield f"data: {pir_state}\n\n"
        time.sleep(0.1)

def get_sensor_data(sensor_pin=PIR_PIN):
    GPIO.setup(sensor_pin, GPIO.IN)
    return GPIO.input(sensor_pin)

def get_frame():
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    frame = stream.getvalue()
    stream.seek(0)
    stream.truncate()
    return frame

def set_servo_pos(pos):
    # setup PWM
    #GPIO.setmode(GPIO.BOARD)

    freq = 50 # PWM frequency in Hz
    duty_min = 2.5 # duty cycle for minimum servo position in percent
    duty_max = 12.5 # duty cycle for maximum servo position in percent

    pwm = GPIO.PWM(SERVO_PIN, freq)
    pwm.start(0)
    duty = duty_min + (pos/180)*(duty_max - duty_min)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3) # wait for servo to reach position

def send_ir_signal(pulses):
    #GPIO.setup(IR_LED_PIN, GPIO.OUT)
    for pulse in pulses:
        GPIO.output(IR_LED_PIN, GPIO.HIGH)
        time.sleep(pulse[0] / 1000000.0)
        GPIO.output(IR_LED_PIN, GPIO.LOW)
        time.sleep(pulse[1] / 1000000.0)

# IR pulses for various off commands
off_signals = {
    'SPEAKERS': [(800, 400), (800, 1600), (800, 400), (800, 1600), (800, 400), (800, 1600)],
    'BLUETOOTH': [(350, 175), (350, 525), (350, 175), (350, 525), (350, 175), (350, 175), (350, 525)],
    'TV': [(9000, 4500), (600, 550), (600, 1700), (600, 550), (600, 1700), (600, 550), (600, 1700), (600, 550), (600, 1700), (600, 550), (600, 550), (600, 550), (600, 550), (600, 550), (600, 550), (600, 1700)],
    'SOUND_BAR': [(9000, 4500), (450, 450), (450, 1300), (450, 450), (450, 1300), (450, 450), (450, 1300), (450, 450), (450, 450), (450, 450), (450, 450), (450, 450), (450, 450), (450, 450), (450, 450), (450, 450), (450, 450), (450, 1300)],
    'AMPLIFIER': [(9000, 4500), (600, 550), (600, 1700), (600, 550), (600, 1700), (600, 550), (600, 1700), (600, 550), (600, 1700), (600, 550), (600, 550), (600, 550), (600, 550), (600, 550), (600, 1700)],
    #'AIR_CONDITIONER': [(3500, 1750), (550, 550), (550, 550), (550, 550), (550, 550), (550, 550), (550, 550), (550, 550), (550, 550), (550, 1650)]
}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
    
    # while True:
    #     if not GPIO.input(SWITCH_PIN):
    #         break
    #     time.sleep(0.1)
    #     print("Switch pressed!")

