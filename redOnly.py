 
import RPi.GPIO as GPIO
import time
import requests

s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10

maxRed = 0
minRed = 100000

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(s2,GPIO.OUT)
  GPIO.setup(s3,GPIO.OUT)
  print("\n")
  

def loop():
  global minRed
  global maxRed
  
  temp = 1
  while(1):  

    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.LOW)
    time.sleep(1)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start 
    red  = NUM_CYCLES / duration   

    print("Read: ( " + str(red) + " )")
    
    #if red > 14000 or green > 10700 or blue > 14000:
    if red > 15000:
      #print("Hay billete, diff: " + str(diff))
      if (maxRed < red):
        maxRed = red
        print("new maxRed: " + str(maxRed))

      if (minRed > red):
        minRed = red
        print("new minRed: " + str(minRed))
      #if green > red:
      #  print("es verde")
      #else:
      #  print("es rojo")
      
    #if green<7000 and blue<7000 and red>12000:
    #  sendData(20)
    #  temp=1
    #elif red<12000 and  blue<12000 and green>12000:
    #  sendData(50)
    #  temp=1
    #elif green<7000 and red<7000 and blue>12000:
    #  sendData(100)
    #  temp=1
    #elif green<7000 and red<7000 and blue>12000:
    #  sendData(200)
    #  temp=1
    #elif green<7000 and red<7000 and blue>12000:
    #  sendData(500)
    #  temp=1
    #elif green<7000 and red<7000 and blue>12000:
    #  sendData(1000)
    #  temp=1
    #elif red>10000 and green>10000 and blue>10000 and temp==1:
    #  print("place the object.....")
    #  temp=0

def sendData(amount):
    print("Sending $" + amount + "...")
    #r = requests.post("http://localhost:5108/api/v1/payment/a275fcb7-3873-47ae-bb70-fe3aa46172a7", data=amount)
    #print(r.status_code, r.reason)
    #print(r.text[:300] + '...')
    time.sleep(5)

def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    
    setup()

    try:
        loop()

    except KeyboardInterrupt:
        print("final maxRed: " + str(maxRed))
        print("final minRed: " + str(minRed))
        endprogram()