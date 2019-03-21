import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep

GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
GPIO.setup(8,GPIO.OUT)    #Ponemos el pin 8 como salida
p = GPIO.PWM(8,50)        #Ponemos el pin 8 en modo PWM y enviamos 50 pulsos por segundo
p.start(2.5)               #Enviamos un pulso del 7.5% para centrar el servo

def setAngle(angle):
    duty = angle /18 + 2
    GPIO.output(8, True)
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(8, False)
    p.ChangeDutyCycle(0)

try:
    while True:      #iniciamos un loop infinito
        p.ChangeDutyCycle(2.5)  # turn towards 0 degree
        print(0)
        time.sleep(1) # sleep 1 second
        p.ChangeDutyCycle(11.5) # turn towards 180 degree
        print(180)
        time.sleep(1) # sleep 1 second 
        
except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    p.ChangeDutyCycle(2.5)  # turn towards 0 degree
    time.sleep(1)
    p.stop()                      #Detenemos el servo
    GPIO.cleanup()                #Limpiamos los pines GPIO de la Raspberry y cerramos el script
