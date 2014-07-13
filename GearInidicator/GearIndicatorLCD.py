import smbus
import time
from PIL import Image


###################################################################
# Class GearIndicatorLCD()
# 
# Interface to the Sh1106 LCD that will be displaying the current 
# gear selection.  The Sh1106 LCD is a 132x64 pixel OLED display.
# Data is displayed on the LCD by alterting the data in the Display
# Data RAM.  The RAM contains a set of bits that correspond to the
# individual pixels of the LCD display. It holds the data in pages 
# and columns.  Their are 8 pages, each representing 8 rows (making up 
# the 64 bit height).  There are 132 columns in each page.  Each page
# is stored as a set of 132 bytes.  The 8 bits of each byte represent
# one of the 8 rows in that page as shown below. The least significant
# bit (D0) represents the top-most row of the page.  The most
# significant bit (D7) represents the bottom-most row of the page.
#
# Changes to the Display Data RAM are immediately reflected on the 
# actual LCD.  When writing bytes to the RAM, the column position is
# automatically incremented with each byte allowing continuous writing
# to memory. The cursor can also be manually set to any position in RAM.
#
#    | Col 0 | Col 1 | Col 2 | ... | Col 131 |
#  ---------------------------------------------------
#    |  D0   |  D0   |               
#  P |  D1   |  D1   |
#  A |  D2   |  D2   |
#  G |  D3   |  D3   |
#  E |  D4   |  D4   |
#    |  D5   |  D5   |
#  0 |  D6   |  D6   | 
#    |  D7   |  D7   |
#  ----------------------------------------------------
#    |  D0   |   
#  P |  D1   |
#  A |  D2   |
#  G |  D3   |
#  E |  D4   |
#    |  D5   |
#  1 |  D6   |
#    |  D7   |
#  ----------------------------------------------------
#
###################################################################
class GearIndicatorLCD():

    def __init__(self):
        #declare i2c specifics
        self.bus = smbus.SMBus(1)
        self.OLED_Address = 0x3c
        self.OLED_Command_Mode = 0x80
        self.OLED_Data_Mode = 0x40


        self.__initialize()
        self.clearScreen()

    ##############################################################
    #initialize()
    #
    #Initilizes the LCD.
    ##############################################################
    def __initialize(self):
        time.sleep(1)
        self.__sendCommand(0xAE)
        self.__sendCommand(0x20)
        self.__sendCommand(0x10)
        self.__sendCommand(0xB0)
        self.__sendCommand(0xC8)

        self.__sendCommand(0x00)
        self.__sendCommand(0x10)
        self.__sendCommand(0x40)

        self.__sendCommand(0x81)
        self.__sendCommand(0x7F)
        self.__sendCommand(0xA1)
        self.__sendCommand(0xA6)
        self.__sendCommand(0xA8)
        self.__sendCommand(0x3F)
        self.__sendCommand(0xA4)
        self.__sendCommand(0xD3)
        self.__sendCommand(0x00)
        self.__sendCommand(0xD5)
        self.__sendCommand(0xF0)
        self.__sendCommand(0xD9)
        self.__sendCommand(0x22)
        self.__sendCommand(0xDA)
        self.__sendCommand(0x12)
        self.__sendCommand(0xDB)
        self.__sendCommand(0x20)
        self.__sendCommand(0x8D)
        self.__sendCommand(0x14)
        self.__sendCommand(0xAF)

        time.sleep(1)

    ############################################################
    #powerUp()
    #
    # Turns on the lighting of the LCD.  Will display whatever
    # is in the Display Data Ram.  Display Data Ram can be
    # altered while the LCD is powered down.
    ############################################################
    def powerUp(self):
        self.__sendCommand(0xA5)

    ############################################################
    #powerDown()
    #
    # Turns of the lighting of the LCD.  LCD will retain
    # whatever is in the Display Data Ram.
    ############################################################
    def powerDown(self):
        self.__sendCommand(0xA4)	# Power off display

    ############################################################
    #clearScreen()
    #
    # Writes 0x00 to every address in the Display Data Ram
    # effectively making the screen completely black.
    # Should be called on first connection of the LCD as
    # when uninitialized the LCD will display random pixels.
    ############################################################
    def clearScreen(self):
        for i in range(8):
                page = 0xB0 + i
                self.__sendCommand(page)
                for i in range(132):
                        self.sendDataByte(0x00)
                self.__sendCommand(0x00)	#reset column address
                self.__sendCommand(0x10)	#reset column address

    ############################################################
    #setCursorPosition(row,col)
    #
    #    row - The row to place the cursor on (0 - 7)
    #    col - The column to place the cursor on (0 - 31)
    #
    ############################################################
    def setCursorPosition(self, row, col):
        rowOffsets = [0x00, 0x40]
        baseOffset = 0x80
        position = baseOffset + rowOffsets[row] + col
        self.__sendCommand(position)


    ##############################################################
    #__sendCommand(command)
    #
    #	command - Hex data to send to the OLED as a command
    #
    #Used to send data to the OLED that should be interpreted as a command, and not display data.
    #Commands are used to control the functions/configuration of the OLED.
    #This method sends the control byte with the D/C Bit set LOW to tell the OLED that the next
    #data sent will be a command
    ##############################################################

    def __sendCommand(self, command):
        self.bus.write_byte_data(self.OLED_Address, self.OLED_Command_Mode, command)
        time.sleep(0.01)

    ###############################################################
    #sendDataByte(dataByte)
    #
    #	data - Hex data to send to the OLED as display data
    #
    ###############################################################

    def __sendDataByte(self, dataByte):
        self.bus.write_byte_data(self.OLED_Address, self.OLED_Data_Mode, dataByte)

    ###############################################################
    #sendData(data)
    #
    #
    ###############################################################
    def __sendData(self, data):
        self.bus.write_i2c_block_data(self.OLED_Address, self.OLED_Data_Mode, data)




    def chunks(self, l, chunkSize):
        for i in xrange(0, len(l), chunkSize):
            yield l[i:i+chunkSize]


    ###############################################################
    #
    #
    #
    ###############################################################
    def displayImage(self, image, colOffset, rowOffset):



    ################################################################
    #displayDigit(filename)
    #
    #
    ################################################################
    def displayDigit(self, filename):
        background = self.processPicture(filename)
        #TODO: Add dimension checking of background image here
        self.__sendCommand(0x13)	#set upper 4 bits of column offset
        self.__sendCommand(0x02)	#set lower 4 bits of column offset
        for i in range(8):
            page = 0xB0 + i
            self.__sendCommand(page)
                #for j in range(132):
                    #	sendDataByte(background[i][j])
            #temp = chunks(background[i], 32)
            #for byteStream in temp:
            #	sendData(byteStream)
            print len(background[i])
            self.__sendData(background[i])
            self.__sendCommand(0x13)	#set upper 4 bits of column offset
            self.__sendCommand(0x02)	#set lower 4 bits of column offseendCommand(0x00)

    ################################################################
    #Class LCDImage
    #
    #    filename - Bitmap file to parse
    #
    # Takes a monochrome bitmap image and represents it in a form
    # that is more easily displayed on the LCD.
    ################################################################
    class LCDImage():

        def __init__(self, filename):

        ###############################################################
        #processPicture(filename)
        #
        #    filename - The bitmap file to import.
        #
        # Imports a monocrhome bitmap file and converts it into a format
        # that can be displayed on the LCD.  The black pixels of the
        # bitmap will be read as "ON", and white as "OFF" effectively
        # reversing the colors on the actual LCD.
        # *The bitmap cannot be larger than 132 pixels wide or 64 pixels
        #  tall.
        # *The bitmap's height must be divisible by 8.
        #
        #    Returns - a (list of lists) that can be passed into
        #        the displayImage(filename)
        ###############################################################
        def processPicture(self, filename):
            output = []
            try:
                picture = Image.open(filename)
                width, height = picture.size
                #Ensure image file will fit within the limits of the LCD
                if(width>132 or height>64):
                    raise ValueError("Picture is larger than the allowable 132x64 pixels.")

                #Ensure image file height is divisible by 8
                #TODO - Should probably just change logic below to properly handle this case.  Don't need it for now.
                if(height % 8 != 0):
                    raise ValueError("Picture height is not divisible by 8.")

                #Read in the picture as a bitstream.
                bits = list(picture.getdata())

                #Convert stream of pixels to width x height array
                matrix = []
                for i in range(height):
                    temp = []
                    for j in range(width):
                        temp.append(bits[i*width + j])
                    matrix.append(temp)

                #Convert width x height array to


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

            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
            except ValueError as e:
                print "Value Error: ", e.value


            return output




#TODO: make an internal class called image which is the array representation of the picutres to display

#################################################
# Testing Below
#################################################
# self.initialize()
# __sendCommand(0x10)
# clearScreen()
# for i in range(4):
# 	displayBackground("shift_1_sized.bmp")
# 	time.sleep(1)
# 	displayBackground("shift_2_sized.bmp")
# 	time.sleep(1)
# 	displayBackground("shift_3_sized.bmp")
# 	time.sleep(1)


