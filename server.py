#!flask/bin/python
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from json import dumps
import RPi.GPIO as GPIO  # Importamos la libreria RPi.GPIO
import time  # Importamos time para poder usar time.sleep
from pusher_push_notifications import PushNotifications

beams_client = PushNotifications(
    instance_id='49348893-bfb2-454f-beeb-d818c7e371fc',
    secret_key='12471EBC914C83D03ADDB856D82E9D5E6EA86EBBAE0C9B9B8998887DF3AF85C6',
)   

GPIO.setmode(GPIO.BOARD)  # Ponemos la Raspberry en modo BOARD
GPIO.setup(8, GPIO.OUT)  # Ponemos el pin 8 como salida
# Ponemos el pin 8 en modo PWM y enviamos 50 pulsos por segundo
p = GPIO.PWM(8, 50)
p.start(7.2)  # Enviamos un pulso del 7.5% para centrar el servo

openDoor = True

green = 11
red = 7

# Indicamos que los pines de los leds son de salida
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

g = GPIO.PWM(green, 1000)
g.start(0)
r = GPIO.PWM(red, 1000)
r.start(0)

app = Flask(__name__)
api = Api(app)


g.ChangeDutyCycle(100)
r.ChangeDutyCycle(0)


@app.route('/open', methods=['POST'])
def open():
    global openDoor
    content = request.get_json()
    p.ChangeDutyCycle(7.2)  # turn towards 0 degree
    g.ChangeDutyCycle(100)
    r.ChangeDutyCycle(100)
    print(0)
    time.sleep(1)
    g.ChangeDutyCycle(100)
    r.ChangeDutyCycle(0)
    print("Oki doki, puerta abierta")
    openDoor = True
    return jsonify({'Open': openDoor})


@app.route('/close', methods=['POST'])
def close():
    global openDoor
    content = request.get_json()
    p.ChangeDutyCycle(2)  # turn towards 180 degree
    g.ChangeDutyCycle(100)
    r.ChangeDutyCycle(100)
    print(180)
    time.sleep(1)  # sleep 1 second
    g.ChangeDutyCycle(0)
    r.ChangeDutyCycle(100)
    print("Puerta cerrada")
    openDoor = False
    return jsonify({'Open': openDoor})


@app.route('/get', methods=['GET'])
def get():
    return jsonify({'Open': openDoor})


@app.route('/sensor', methods=['GET'])
def sensor():
    global openDoor
    if (not openDoor):
        response = beams_client.publish_to_interests(
            interests=['hello'],
            publish_body={
                'apns': {
                    'aps': {
                        'alert': 'Puerta abierta',
                    },
                },
                'fcm': {
                    'notification': {
                        'title': 'Puerta abierta',
                        'body': 'La puerta se ha abierto',
                    },
                },
            },
        )

        print(response['publishId'])
    return jsonify({'Open': openDoor})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
