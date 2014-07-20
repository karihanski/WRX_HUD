# from Sh1106.GearIndicatorLCD import *
# from I2CConfig import *
# from WideHKOLED.WideHKOLED import *
# from threading import Thread
from SSM.pimonitor.PMXmlParser import *
import traceback
import time


# def cycleGears():
#     while True:
#         for i in range(0,5):
#             gearIndicator.displayGear(i)
#             time.sleep(2)
#
# def flopText():
#     while True:
#         dataDisplay.sendString("HelloWorld", 0, 0)
#         time.sleep(1)
#         dataDisplay.clearScreen()
#         dataDisplay.sendString("HelloWorld", 1, 0)
#         time.sleep(1)
#         dataDisplay.clearScreen()
#
# def concurrentTest():
#     #Initialize Gear Indicator on I2C 1
#     gearIndicator = GearIndicatorLCD()
#
#     #Initialize I2C 0
#     i2cConfig()
#
#     #Initialize digit display on I2C 0
#     dataDisplay = WideHKOLED()
#
#     #Test the output to both displays.
#     try:
#         Thread(target=cycleGears).start()
#         Thread(target=flopText()).start()
#
#     except:
#         print "Cannot start thread"
import array
import os
import os.path
import time
import cPickle as pickle

from SSM.pimonitor.PM import PM
from SSM.pimonitor.PMConnection import PMConnection
from SSM.pimonitor.PMPacket import PMPacket
from SSM.pimonitor.PMParameter import PMParameter
from SSM.pimonitor.PMUtils import PMUtils
from SSM.pimonitor.PMXmlParser import PMXmlParser


if __name__=="__main__":





    parser = PMXmlParser()

    supported_parameters = []

    defined_parameters = parser.parse("logger_METRIC_EN_v131.xml")

    connection = PMConnection()

    while True:
        try:


            connection.open()
            #Query ecu/tcu to see which parameters are supported.
            ecu_packet = connection.init(1)
            tcu_packet = connection.init(2)

            if ecu_packet == None or tcu_packet == None:
                print "Can't get initial data."
                continue

            #Match the defined parameters against which ones are in teh ecu/tcu supported parameters
            for p in defined_parameters:
                if (p.get_target() & 0x1 == 0x1) and p.is_supported(ecu_packet.to_bytes()[5:]):
                    if not filter(lambda x: x.get_id() == p.get_id(), supported_parameters):
                        supported_parameters.append(p)

            for p in defined_parameters:
                if ((p.get_target() & 0x2 == 0x2) or (p.get_target() & 0x1 == 0x1)) and p.is_supported(tcu_packet.to_bytes()[5:]):
                    if not filter(lambda x: x.get_id() == p.get_id(), supported_parameters):
                        supported_parameters.append(p)

            for p in defined_parameters:
                p_deps = p.get_dependencies()
                if not p_deps:
                    continue

                deps_found = ()
                for dep in p_deps:
                    deps_found = filter(lambda x: x.get_id() == dep, supported_parameters)
                    if not deps_found:
                        break

                    if len(deps_found) > 1:
                        raise Exception('duplicated dependencies', deps_found)

                    p.add_parameter(deps_found[0])

                if deps_found:
                    supported_parameters.append(p)

            # each ID must be in a form P01 - first letter, then a number
            supported_parameters.sort(key=lambda p: int(p.get_id()[1:]), reverse=False)

         #   print "==================================="
          #  print "Supported Parameters Below:"
           # print "==================================="
            #Print out the supported parameters
            # for p in supported_parameters:
            #     print p.to_string()

            #Find the rpm+
            rpm_parameter = supported_parameters.get
            packets = connection.read_parameters(parameters)

        except IOError as e:
            traceback.print_exc()
            print "I/O error: {0} {1}".format(e.errno, e.strerror)

            if connection != None:
                connection.close()
                time.sleep(3)
            continue

    connection.close()