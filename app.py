from platform import dist
from flask import Flask, render_template
from pushbullet import Pushbullet
import RPi.GPIO as GPIO
import time
import Adafruit_DHT

app = Flask(__name__)

urls = (
    '/testindigo.png', 'bg'
    '/breadboard.jpg', 'bb'
    '/pi4b.png', 'pi4b'
    '/DHT22_pins.jpg', 'dht22'
    '/senzor.jpg', 'hcsr04'
    '/dhtpi.png', 'dhtpi'
    '/hcpi.png', 'hcpi'
    '/tmp-svg.svg', 'svg1'
    '/drop.svg', 'svg2'
    '/bggrey.jpg', 'gbg'
     )

class bgg:
    def GET(self): raise app.seeother("/static/bggrey.jpg")

class svg2:
    def GET(self): raise app.seeother("/static//drop.svg")

class svg1:
    def GET(self): raise app.seeother("/static/tmp-svg.svg")

class bg:
    def GET(self): raise app.seeother("/static/testindigo.png")

class bb:
    def GET(self): raise app.seeother("/static/breadboard.jpg")

class pi4b:
    def GET(self): raise app.seeother("/static/pi4b.png")

class dht22:
    def GET(self): raise app.seeother("/static/DHT22_pins.jpg")

class hcsr04:
    def GET(self): raise app.seeother("/static/senzor.jpg")
class dhtpi:
    def GET(self): raise app.seeother("/static/dhtpi.png")
class hcpi:
    def GET(self): raise app.seeother("/static/hcpi.png")


pb = Pushbullet("o.qNrLP4GqlGZBHo5tBqM1tNRg2WBMAX9r")
sensor = Adafruit_DHT.DHT22

#pins
sensor_pin = 4
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def percentage(distance):
    distancePercent = distance/120*100
    if distancePercent > 100 :
        distancePercent = 100
    return distancePercent

@app.route('/')
def index():
    GPIO.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    #StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    #time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    
    
    if percentage(distance) > 80 : 
      dev = pb.get_device('HUAWEI ELE-L29')
      push = dev.push_note("Alert!!", "isprazni kantu")
   
    #dht22 
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

    
    templateData = {'distance' : format(percentage(distance), ".2f"),
                    'humidity' : format(humidity, ".2f"),
                    'temperature' : format(temperature, ".2f")}
                    
    return render_template('index.html', **templateData)

@app.route('/garbage')
def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    #StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    #time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    
    
    if percentage(distance) > 80 : 
      dev = pb.get_device('HUAWEI ELE-L29')
      push = dev.push_note("Alert!!", "isprazni kantu")
   
    #dht22 
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

    
    templateData = {'distance' : format(percentage(distance), ".2f"),
                    'humidity' : format(humidity, ".2f"),
                    'temperature' : format(temperature, ".2f")}

    return render_template('garbage.html', **templateData)

@app.route('/projekt')
def projekt():
   return render_template('projekt.html')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')