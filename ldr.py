import RPi.GPIO as GPIO
import time
import os

#Expresión lambda que limipia la consola
clear = lambda: os.system('clear')
#Indicamos a GPIO que vamos a nombrar a los pines por su número 
GPIO.setmode(GPIO.BOARD)

#Variable donde indicamos el limite de luz detectada en la 
# que hacemos que los colores cambien
limit = 40

#Asignamos los números de los pines donde tenemos conectados 
# los leds y el LDR a variables
ldr = 10

green = 11
blue = 13
red = 7

#Indicamos que los pines de los leds son de salida
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

#Creamos un objeto PMW en los pines de cada led y los iniciamos
# a 0 es decir apagados
g = GPIO.PWM(green, 1000)
g.start(0)
b = GPIO.PWM(blue, 1000)
b.start(0)
r = GPIO.PWM(red, 1000)
r.start(0)

redValue = 50
blueValue = 50

light = 0

#Función que nos devuelve el valor de luz que detecta el LDR
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
    clear()
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
        else: # Si hay poca luz subimos la luz azul y bajamos la luz roja
            for dc in range(blueValue, value, 5):
                b.ChangeDutyCycle(dc)
                blueValue = dc
                r.ChangeDutyCycle(100-dc)
                redValue = 100-dc
                time.sleep(0.05)

        # Limpiamos la pantalla y mostramos los valores de luz detectada por el LDR
        # y al porcentaje que están funcionando los leds        
        clear()
        print('\033[95m' + "Ldr: "+str(light))
        print('\033[94m' + "Azul: "+str(blueValue)+"%")
        print('\033[91m' + "Rojo: "+str(redValue)+"%")

# Si se interrumpe la señal se apagan los leds
except KeyboardInterrupt:
    print('\033[1;37;40m')
    b.stop()
    g.stop()
    r.stop()

    GPIO.output(green, GPIO.HIGH)
    GPIO.output(blue, GPIO.HIGH)
    GPIO.output(red, GPIO.HIGH)

    print("Clean up")
    GPIO.cleanup()