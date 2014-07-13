import smbus
import time

#declare i2c specifics
bus = smbus.SMBus(1)
OLED_Address = 0x3c
OLED_Command_Mode = 0x80
OLED_Data_Mode = 0x40



def init():
	time.sleep(1)
	sendCommand(0x2A)
	sendCommand(0x71)
	sendCommand(0x5C)
 	sendCommand(0x28)

 	sendCommand(0x08)	
 	sendCommand(0x2A)	# **** Set "RE"=1	00101010B
 	sendCommand(0x79)	# **** Set "SD"=1	01111001B

 	sendCommand(0xD5)
 	sendCommand(0x70)
 	sendCommand(0x78)	# **** Set "SD"=0  01111000B

 	sendCommand(0x08)	# **** Set 5-dot, 3 or 4 line(0x09), 1 or 2 line(0x08)

 	sendCommand(0x06)	# **** Set Com31-->Com0  Seg0-->Seg99

 	# **** Set OLED Characterization *** #
 	sendCommand(0x2A) 	# **** Set "RE"=1 
 	sendCommand(0x79)  	# **** Set "SD"=1

 	# **** CGROM/CGRAM Management *** #
 	sendCommand(0x72)  	# **** Set ROM
 	sendCommand(0x00)  	# **** Set ROM A and 8 CGRAM


 	sendCommand(0xDA) 	# **** Set Seg Pins HW Config
 	sendCommand(0x10)   

 	sendCommand(0x81)  	# **** Set Contrast
 	sendCommand(0xFF) 

 	sendCommand(0xDB)  	# **** Set VCOM deselect level
 	sendCommand(0x30)  	# **** VCC x 0.83

 	sendCommand(0xDC)  	# **** Set gpio - turn EN for 15V generator on.
 	sendCommand(0x03)

 	sendCommand(0x78)  	# **** Exiting Set OLED Characterization
 	sendCommand(0x28) 
 	sendCommand(0x2A) 
 	#sendCommand(0x05); 	# **** Set Entry Mode
 	sendCommand(0x06) 	# **** Set Entry Mode
 	sendCommand(0x08)  
 	sendCommand(0x28) 	# **** Set "IS"=0 , "RE" =0 #28
 	sendCommand(0x01) 
 	sendCommand(0x80) 	# **** Set DDRAM Address to 0x80 (line 1 start)

	time.sleep(0.1)
	sendCommand(0x0C)	# Turn on display


def powerUp():
	time.sleep(1)
	sendCommand(0x0C)

def powerDown():
	time.sleep(1)
	sendCommand(0x08)	# Power off display

def clearScreen():
	sendCommand(0x01)
	time.sleep(0.1)

def setCursorPosition(row, col):
	rowOffsets = [0x00, 0x40]
	baseOffset = 0x80
	position = baseOffset + rowOffsets[row] + col
	sendCommand(position)


"""
sendCommand(command)

	command - Hex data to send to the OLED as a command

Used to send data to the OLED that should be interpreted as a command, and not display data.
Commands are used to control the functions/configuration of the OLED.
This method sends the control byte with the D/C Bit set LOW to tell the OLED that the next
data sent will be a command
""" 

def sendCommand(command):
	bus.write_byte_data(OLED_Address, OLED_Command_Mode, command)
	time.sleep(0.01)
	
"""
sendData(data)

	data - Hex data to send to the OLED as display data

"""

def sendData(data):
	bus.write_byte_data(OLED_Address, OLED_Data_Mode, data)
	time.sleep(0.01)

"""
sendString(text, row, col)

	text - The string that you want to display
	row - The row on which to begin printing the string (0 is upper, 1 is lower)
	col - the position within the row to start printing the string (0 to 15)

Sends a string to the lcd to be displaced at the cursor position indicated
"""

def sendString(text, row, col):
	setCursorPosition(row, col)
	for char in text:
		sendData(int(hex(ord(char)), 16))

	


#init()	
clearScreen()
time.sleep(1)

string = "Flash"
sendString(string, 1, 7)

powerDown()
