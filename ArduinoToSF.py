import os
import sys
import RPi.GPIO as GPIO
import json
import requests
import dhtreader
import time
from simple_salesforce import Salesforce
from simple_salesforce import SalesforceLogin
from simple_salesforce import SFType

GPIO.setmode(GPIO.BCM)

type = 11
pin = 24

sf = Salesforce(username='xxxxxxxxxx', 
	password='xxxxxxxx', security_token='xxxxxxxxxx', sandbox=False)

session_id, instance = SalesforceLogin(username='xxxxxxxxxx', 
	password='xxxxxxxxxx', security_token='xxxxxxxxxxxxxxxxx', sandbox=False)

testReading = SFType('testReadingPy__c', session_id=session_id,
                     sf_instance='na17.salesforce.com', sf_version='32.0', proxies=None)

def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(RCpin, GPIO.IN)

    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return 100-(reading/10)

while True:
	dhtreader.init()
	output = dhtreader.read(type,pin)
	lightval = str(RCtime(17))
	if output!=None:
		output=str(output)
		output=output[1:-1]
		output=output.translate(None, ',')
		output = output + ' ' + lightval
		a,b,c = output.split(" ")
		print a+b+c
		testReading.create({'Temperature_Reading__c' : a, 'Humidity_Reading__c' : b, 'Light_Reading__c' : c, 'Hidden_Sensor_Index__c' : 'xxxxxxxxxx'})
		time.sleep(1800)
