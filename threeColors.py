import RPi.GPIO as GPIO
import time
import requests

s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(s2,GPIO.OUT)
  GPIO.setup(s3,GPIO.OUT)
  print("\n")
  

def loop():
  temp = 1
  while(1):  

    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.LOW)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start 
    red  = NUM_CYCLES / duration   
   
    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    

    GPIO.output(s2,GPIO.HIGH)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration

    print("Read: (", red, ", ", green, ", ", blue, ")")
    
    #if red > 14000 or green > 10700 or blue > 14000:
    if red > 23000 and green > 17300 and blue > 23000:
      if red > green and red > blue:
          sendData(50)
      elif green > red and green > blue:
          sendData(200)
      elif blue > red and blue > green:
          sendData(500)
      

def sendData(amount):
    amountStr = str(amount)
    headers = {'Content-Type': 'application/json'}
    print("Sending $" + amountStr + "...")
    r = requests.post("http://165.227.53.110:5108/api/v1/payment/a275fcb7-3873-47ae-bb70-fe3aa46172a7", data="100", headers=headers)
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
    time.sleep(5)

def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    
    setup()

    try:
        loop()

    except KeyboardInterrupt:
        endprogram() 
