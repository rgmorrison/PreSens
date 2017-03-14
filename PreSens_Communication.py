#Ryan Morrison
#2-24-17
#Script to talk with EOM-O2-FDM-SMA sesnor

#add log file .txt or .csv

import time
import serial
import RPi.GPIO as GPIO ## Import GPIO library

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(38, GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
GPIO.setup(40, GPIO.OUT)   ## Setup GPIO Pin to OUTPUT


####################################################################################
#                 Configuring the Serial Ports and other variables
####################################################################################
#configure the serial communication for EOM-O2-FDM-SMA oxygen sensor
ser = serial.Serial()
ser.port = "COM8"
ser.baudrate = 19200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 0
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 0

#Set oxygen unit output
#0000 - % air saturation (default)
#0001 - %O2  #use this
#0002 - hPa
#0003 - Torr
#0004 - mg/L , ppm*
#0005 - umol/L
#0006 - ppm gas*
oxygen_unit = 6
####################################################################################



####################################################################################
#                             Opening the Serial Ports
####################################################################################
#Wait for device initialization to complete max time = 16s
#convert to milliseconds
time.sleep(16)

#attempts to open the serial port 
try: 
    ser.open()
    print("Attempting to open ports: " + str(ser.portstr))

#If there is an exeption raised when trying to open the COM ports,    
except Exception as e:
    print ("Error, " + str(e))

#If the serial ports are open,    
if ser.is_open:
    print("Successfully opened: " + str(ser.portstr))
####################################################################################



####################################################################################
#                 Commands to be sent once to EOM-O2-FDM-SMA
####################################################################################    
    #Set the EOM-O2-FDM-SMA sesnor oxygen unit
    try:
        ser.write('oxyu000' + str(oxygen_unit) + '\r')
    except Exception as e1:
        print ("Error communicating...: " + str(e1))
####################################################################################

        
####################################################################################
#                Continuous Data Requests to EOM-O2-FDM-SMA
#################################################################################### 
    run_time = time.time() + 10 #seconds

    #Runs while loop for 10 seconds
    while time.time() < run_time:
        try:
            #Send data request
            ser.write('data\r')
            #Give device time to respond in seconds minimum ~300ms
            time.sleep(400)


            #Read the response
            response = ser.read(ser.inWaiting())
            print("Response: " + str(response))


            #Split the response string
            splitresponse = response.split(";")
            device_number = splitresponse[0]
            amplitude = splitresponse[1]
            phase_shift = splitresponse[2]
            compensation_temperature = splitresponse[3]
            oxygen = splitresponse[4]
            error_response = splitresponse[5]
            pressure = splitresponse[6]

            #Correcting the ouput data into readable data
            oxygen = str(int(oxygen[:5])) + '.' + oxygen[6:] 

        #If there is an exception raised while sending the commands,
        except Exception as e2:
            print ("Error communicating...: " + str(e2))


        #Open the motor valve
        if oxygen >= 10:
            GPIO.output(38, True) ## State is true/false
            time.sleep(0.25)
            GPIO.output(38, False) ## State is true/false

        #Close the motor valve
        elif oxygen <= 10:
            GPIO.output(40, True) ## State is true/false
            time.sleep(0.25)
            GPIO.output(40, False) ## State is true/false
            
        
            
####################################################################################
    #Close the serial ports                
    ser.close()
    print("Closed: " + str(ser.portstr) )


#If the serial ports are not able to be opened,
else:
    print ("Problem with opening one of the serial ports ")
