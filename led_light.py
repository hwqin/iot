import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
ledPin1 = 16
ledPin2 = 8


GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin2, GPIO.OUT)

for i in range(5):
  print("LED turning on.")
  GPIO.output(ledPin1, GPIO.HIGH)
  time.sleep(0.5)
  print("LED turning off.")
  GPIO.output(ledPin1, GPIO.LOW)
  time.sleep(0.5)
  print("LED turning on.")
  GPIO.output(ledPin2, GPIO.HIGH)
  time.sleep(0.5)
  print("LED turning off.")
  GPIO.output(ledPin2, GPIO.LOW)
  time.sleep(0.5)
