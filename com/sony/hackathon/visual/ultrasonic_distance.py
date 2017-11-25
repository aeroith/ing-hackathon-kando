import RPi.GPIO as GPIO
from beep import beep
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
  
#set GPIO Pins
GPIO_TRIGGER_R = 15
GPIO_ECHO_R = 14
GPIO_TRIGGER_L = 24
GPIO_ECHO_L = 23
   
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_R, GPIO.OUT)
GPIO.setup(GPIO_ECHO_R, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_L, GPIO.OUT)
GPIO.setup(GPIO_ECHO_L, GPIO.IN) 
    
def distanceRight():
        GPIO.output(GPIO_TRIGGER_R, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER_R, False)
        StartTime_R = time.time()
        StopTime_R = time.time()
        while GPIO.input(GPIO_ECHO_R) == 0:
            StartTime_R = time.time()
        while GPIO.input(GPIO_ECHO_R) == 1:
            StopTime_R = time.time()
        TimeElapsed_R = StopTime_R - StartTime_R
        distance_R = (TimeElapsed_R * 34300) / 2
        return distance_R
def distanceLeft():
        GPIO.output(GPIO_TRIGGER_L, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER_L, False)
        StartTime_L = time.time()
        StopTime_L = time.time()
        while GPIO.input(GPIO_ECHO_L) == 0:
            StartTime_L = time.time()
        while GPIO.input(GPIO_ECHO_L) == 1:
            StopTime_L = time.time()
        TimeElapsed_L = StopTime_L - StartTime_L
        distance_L = (TimeElapsed_L * 34300) / 2
        return distance_L
        
                                                                                                       
if __name__ == '__main__':
        try:
            while True:
                dist_R = distanceRight()
                dist_L = distanceLeft()
                distList = [dist_R, dist_L]
                distMin = min(distList)
                print ("******************************************")
                print ("Right = %.1f cm" % dist_R)
                print ("******************************************")
                print ("******************************************")
                print ("Left = %.1f cm" % dist_L)
                print ("******************************************")
                print ("MINIMUM = %.1f cm" % distMin)
                beep(distMin)
                                                                                                                                               # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()

