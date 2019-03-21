#!flask/bin/python
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from json import dumps
import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep

GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
GPIO.setup(8,GPIO.OUT)    #Ponemos el pin 8 como salida
p = GPIO.PWM(8,50)        #Ponemos el pin 8 en modo PWM y enviamos 50 pulsos por segundo
p.start(2.5)               #Enviamos un pulso del 7.5% para centrar el servo

green = 11
red = 7

#Indicamos que los pines de los leds son de salida
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

g = GPIO.PWM(green, 1000)
g.start(0)
r = GPIO.PWM(red, 1000)
r.start(0)

app = Flask(__name__)
api = Api(app)

@app.route('/open', methods=['POST'])
def open():
    content = request.get_json()
    p.ChangeDutyCycle(2.5)  # turn towards 0 degree
    g.ChangeDutyCycle(100)
    r.ChangeDutyCycle(100)
    print(0)
    time.sleep(1)
    g.ChangeDutyCycle(100)
    r.ChangeDutyCycle(0)
    print(content["text"])
    return content["text"]
@app.route('/close', methods=['POST'])
def close():
    content = request.get_json()
    p.ChangeDutyCycle(7.5) # turn towards 180 degree
    g.ChangeDutyCycle(100)
    r.ChangeDutyCycle(100)
    print(180)
    time.sleep(1) # sleep 1 second 
    g.ChangeDutyCycle(0)
    r.ChangeDutyCycle(100)
    print(content["text"])
    return content["text"]

if __name__ == '__main__':
    app.run(host='0.0.0.0')