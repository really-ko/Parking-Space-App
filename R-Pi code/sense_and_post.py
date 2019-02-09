''' 
 Date: Feb. 9th 2019
 Author: Isaac Chen
 Purpose: read ultrasonic sensors and post status to mqtt
'''

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(self, client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    self.publish("ParKar", "ParKar is connected")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	command = str(msg.payload)
	print(msg.topic+" "+ command)
	
client = mqtt.Client(client_id="test")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("hgyfcdvp","7xO7C0uC6s-U")
client.connect("m16.cloudmqtt.com", 17657, 60)

try:
	GPIO.setmode(GPIO.BOARD)
	
	PIN_TRI1 = 7
	PIN_ECHO1 = 11
	PIN_TRI2 = 13
	PIN_ECHO2 = 15
	
	GPIO.setup(PIN_TRI1, GPIO.OUT)
	GPIO.setup(PIN_ECHO1, GPIO.IN)
	GPIO.setup(PIN_TRI2, GPIO.OUT)
	GPIO.setup(PIN_ECHO2, GPIO.IN)
	
	# resetting the tri port
	GPIO.output(PIN_TRI1, GPIO.LOW)
	GPIO.output(PIN_TRI2, GPIO.LOW)
	time.sleep(2)
	print("settling Tris ...")
	
	while 1:
		# send Tri1 signal
		GPIO.output(PIN_TRI1,GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(PIN_TRI1,GPIO.LOW)
		
		# Echo1 receive
		while GPIO.input(PIN_ECHO1) == 0:
			start_time1 = time.time()
		while GPIO.input(PIN_ECHO1) == 1:
			end_time1 = time.time()
		
		# send Tri2
		GPIO.output(PIN_TRI2,GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(PIN_TRI2,GPIO.LOW)
		
		# Echo2 receive
		while GPIO.input(PIN_ECHO2) == 0:
			start_time2 = time.time()
		while GPIO.input(PIN_ECHO2) == 1:
			end_time2 = time.time()
		
		# Calculating distance
		duration1 = end_time1 - start_time1
		duration2 = end_time2 - start_time2
		
		distance1 = round(duration1 * 17150, 2)
		distance2 = round(duration2 * 17150, 2)
		
		print("D1: ",distance1)
		print("D2: ",distance2)
		if distance1 < 25:
			print("spot 1 taken")
			client.publish("Calvin/Parkinglot14/row1/spot1","taken")
		if distance1 >= 25:
			print("spot 1 available")
			client.publish("Calvin/Parkinglot14/row1/spot1","available")
		if distance2 < 25:
			print("spot 2 taken")
			client.publish("Calvin/Parkinglot14/row1/spot2","taken")
		if distance2 >= 25:
			print("spot 2 available")
			client.publish("Calvin/Parkinglot14/row1/spot2","available")
			
		time.sleep(5);
		
finally:
	GPIO.cleanup()
	
