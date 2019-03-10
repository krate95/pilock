import RPi.GPIO as GPIO
import time
import os

clear = lambda: os.system('clear')
GPIO.setmode(GPIO.BOARD)

limit = 40

ldr = 10

green = 11
blue = 13
red = 7

GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

g = GPIO.PWM(green, 1000)
g.start(0)
b = GPIO.PWM(blue, 1000)
b.start(0)
r = GPIO.PWM(red, 1000)
r.start(0)

redValue = 50
blueValue = 50

light = 0

def timer (pin):
    reading = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    while (GPIO.input(pin) == GPIO.LOW):
        reading += 1
    return reading

try:
    print("Inicializados los tres leds a 50%")
    g.ChangeDutyCycle(50)
    r.ChangeDutyCycle(redValue)
    b.ChangeDutyCycle(blueValue)
    time.sleep(5)
    
    while True:
        value = timer(ldr)
        light = value
        if(value > 1000):
            value = 1000
        value = value//10
        if (value < limit):  # Si hay mucha luz baja la luz azul y sube la roja
            for dc in range(blueValue, value, -5):
                b.ChangeDutyCycle(dc)
                blueValue = dc
                r.ChangeDutyCycle(100-dc)
                redValue = 100-dc
                time.sleep(0.05)
        else:
            for dc in range(blueValue, value, 5):
                b.ChangeDutyCycle(dc)
                blueValue = dc
                r.ChangeDutyCycle(100-dc)
                redValue = 100-dc
                time.sleep(0.05)

                
        clear()
        print("Ldr: "+str(light))
        print("Azul: "+str(blueValue)+"%")
        print("Rojo: "+str(redValue)+"%")

except KeyboardInterrupt:
    b.stop()
    g.stop()
    r.stop()

    GPIO.output(green, GPIO.HIGH)
    GPIO.output(blue, GPIO.HIGH)
    GPIO.output(red, GPIO.HIGH)

    print("Clean up")
    GPIO.cleanup()