import RPi.GPIO as GPIO
import MFRC522
import signal
import requests
from time import sleep

URL = "http://172.17.2.10:3000/api/rfidReader"

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted


def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the RFID Reader"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected: "

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID

	if uid[0] == 80 :
		print "You get the first tip!"
		payload = {
            		"devID": "RFID-READER",
            		"value": "IT IS VERY IMPORTANT TO LISTEN, SO LISTEN TO THE MAZE. HE MAY HELP YOU."
        		}

	elif uid[0] == 143 :
#		print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
		print "You get the second tip!"
		payload = {
			"devID": "RFID-READER",
			"value": "STEP BY STEP, LAYER BY LAYER..."
			}

        # This is the default key for authentication
	key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(
            MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"

        try:
            response = requests.request("POST", URL, data=payload)
            print(response.text)
        except:
            print("data not POSTED")
        sleep(5)
