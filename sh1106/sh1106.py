import smbus
import time
from PIL import Image

#declare i2c specifics
bus = smbus.SMBus(1)
OLED_Address = 0x3c
OLED_Command_Mode = 0x80
OLED_Data_Mode = 0x40



def init():
	time.sleep(1)
	sendCommand(0xAE)
	sendCommand(0x20)	#Set memory addressing mode
	sendCommand(0x10)	#
	sendCommand(0xB0)
	sendCommand(0xC8)

	sendCommand(0x00)
	sendCommand(0x10)
	sendCommand(0x40)

	sendCommand(0x81)
	sendCommand(0x7F)
	sendCommand(0xA1)
	sendCommand(0xA6)
	sendCommand(0xA8)
	sendCommand(0x3F)
	sendCommand(0xA4)
	sendCommand(0xD3)
	sendCommand(0x00)
	sendCommand(0xD5)
	sendCommand(0xF0)
	sendCommand(0xD9)
	sendCommand(0x22)
	sendCommand(0xDA)
	sendCommand(0x12)
	sendCommand(0xDB)
	sendCommand(0x20)
	sendCommand(0x8D)
	sendCommand(0x14)
	sendCommand(0xAF)
	
	time.sleep(1)


def powerUp():
	sendCommand(0xA5)

def powerDown():
	sendCommand(0xA4)	# Power off display

def clearScreen():
	for i in range(8):
        	page = 0xB0 + i
        	sendCommand(page)
        	for i in range(132):
                	sendDataByte(0x00)
        	sendCommand(0x00)	#reset column address
        	sendCommand(0x10)	#reset column address

def setCursorPosition(page, col):
	rowOffsets = [0x00, 0x40]
	baseOffset = 0x80
	position = baseOffset + rowOffsets[row] + col
	sendCommand(position)


##############################################################
#sendCommand(command)
#
#	command - Hex data to send to the OLED as a command
#
#Used to send data to the OLED that should be interpreted as a command, and not display data.
#Commands are used to control the functions/configuration of the OLED.
#This method sends the control byte with the D/C Bit set LOW to tell the OLED that the next
#data sent will be a command
############################################################## 

def sendCommand(command):
	bus.write_byte_data(OLED_Address, OLED_Command_Mode, command)
	time.sleep(0.01)
	
###############################################################
#sendDataByte(dataByte)
#
#	data - Hex data to send to the OLED as display data
#
###############################################################

def sendDataByte(dataByte):
	bus.write_byte_data(OLED_Address, OLED_Data_Mode, dataByte)

###############################################################
#sendData(data)
#
#
###############################################################
def sendData(data):
	bus.write_i2c_block_data(OLED_Address, OLED_Data_Mode, data)



def processPicture(filename):
	picture = Image.open(filename)
	width, height = picture.size
	bits = list(picture.getdata())
	
	#TODO - PUT SOME ERROR CHECKING IN HERE (LIST LENGTH, Ensure that picture height is divisible by 8 ETC.)

	#Convert stream of pixels to width x height array
	matrix = []
	for i in range(height):
		temp = []
		for j in range(width):
			temp.append(bits[i*width + j])
		matrix.append(temp)

	output = []

	for i in range(height/8):
		temp = []
		for j in range(width):
			bit0 = (matrix[i*8][j] / 255)
			bit1 = 2 * (matrix[i*8 + 1][j] / 255)
			bit2 = 4 * (matrix[i*8 + 2][j] / 255)
			bit3 = 8 * (matrix[i*8 + 3][j] / 255)
			bit4 = 16 * (matrix[i*8 + 4][j] / 255)
			bit5 = 32 * (matrix[i*8 + 5][j] / 255)
			bit6 = 64 * (matrix[i*8 + 6][j] / 255)
			bit7 = 128 * (matrix[i*8 + 7][j] / 255)
			temp.append(bit0 + bit1 + bit2 + bit3 + bit4 + bit5 + bit6 + bit7)
		output.append(temp)

	return output

def chunks(l, chunkSize):
	for i in xrange(0, len(l), chunkSize):
		yield l[i:i+chunkSize]


def displayBackground(filename):
	background = processPicture(filename)
	#TODO: Add dimension checking of background image here
	sendCommand(0x13)	#set upper 4 bits of column offset
	sendCommand(0x02)	#set lower 4 bits of column offset
	for i in range(8):
       		page = 0xB0 + i
        	sendCommand(page)
        	#for j in range(132):
                #	sendDataByte(background[i][j])
		#temp = chunks(background[i], 32)
		#for byteStream in temp:
		#	sendData(byteStream)
		print len(background[i])
		sendData(background[i])
        	sendCommand(0x13)	#set upper 4 bits of column offset
		sendCommand(0x02)	#set lower 4 bits of column offseendCommand(0x00)

#def displayImage(image, )
	


#################################################
# Testing Below
#################################################
init()
sendCommand(0x10)
clearScreen()
for i in range(4):
	displayBackground("shift_1_sized.bmp")
	time.sleep(1)
	displayBackground("shift_2_sized.bmp")
	time.sleep(1)
	displayBackground("shift_3_sized.bmp")
	time.sleep(1)


