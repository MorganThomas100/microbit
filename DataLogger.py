from microbit import *
import os

#todo no globals please
sampleMillis = 500
sampleMillisTotal = 0
sampleMillisMax = 1000 * 10000
filename = 'data.csv'
displayStartSequenceMillis = 300
displayEndSequenceMillis = 200
returnStr = '\r\n'
accelCalibrationXOffset = 0
accelCalibrationYOffset = 0
accelCalibrationZOffset = 0


imageA = Image("99999:"
               "99999:"
               "99999:"
               "99999:"
               "99999")
              
imageB = Image("00000:"
               "09990:"
               "09990:"
               "09990:"
               "00000")

imageC = Image("00000:"
               "00000:"
               "00900:"
               "00000:"
               "00000")

imageD = Image("00000:"
               "00000:"
               "00000:"
               "00000:"
               "00000")
# functions

def DisplayFileSystem():
    local_files = os.listdir()
    fileCount = len(local_files)
    #check number of files
    uart.write('File System - found ' + str(fileCount) + ' files' + returnStr)
    for fileDesc in enumerate(local_files):
        uart.write(str(fileDesc) + returnStr)
    uart.write('Finished File System State' + returnStr)

def ClearFileSystem():
    local_files = os.listdir()
    fileCount = len(local_files)
    uart.write('File System - found ' + str(fileCount) + ' files' + returnStr)
    for fileDesc in enumerate(local_files):
        #not working cannot convert tuple
        #os.remove(fileDesc)
        uart.write(str(fileDesc) + returnStr)
    uart.write('Cleared File System' + returnStr)

def DisplayStartSequence():
    display.show("3")
    sleep(displayStartSequenceMillis)
    display.show("2")
    sleep(displayStartSequenceMillis)
    display.show("1")
    sleep(displayStartSequenceMillis)
    display.show("")

def DisplayEndSequence():
    count = 0
    while (count < 10):
        display.show(imageA)
        sleep(displayEndSequenceMillis)
        display.show(imageB)
        sleep(displayEndSequenceMillis)
        display.show(imageC)
        sleep(displayEndSequenceMillis)
        display.show(imageD)
        sleep(displayEndSequenceMillis)
        count = count + 1

def CreateLoggerEntry():
    dataLine = str(sampleMillisTotal) + ','
    dataLine = dataLine + str(accelerometer.get_x() - accelCalibrationXOffset) + ','
    dataLine = dataLine + str(accelerometer.get_y() - accelCalibrationYOffset) + ','
    dataLine = dataLine + str(accelerometer.get_z() - accelCalibrationZOffset) + ','
    return dataLine + '\n\r'

def CalibrateAccelerometer():
    calibrateMillisTotal = 0
    calibrateMillisMax = 5000
    calibrateMillis = 100

    calibrationCounter = 0
    xSum = 0
    ySum = 0
    zSum = 0
    while (calibrateMillisTotal <= calibrateMillisMax):
        xSum = xSum + accelerometer.get_x()
        ySum = ySum + accelerometer.get_y()
        zSum = zSum + accelerometer.get_z()
        calibrationCounter = calibrationCounter + 1
        calibrateMillisTotal = (calibrateMillisTotal + calibrateMillis)

    accelCalibrationXOffset = xSum / calibrationCounter
    accelCalibrationYOffset = ySum / calibrationCounter
    accelCalibrationZOffset = zSum / calibrationCounter

    uart.write('Accelerometer Calibrated' + returnStr)
    uart.write('X = ' + str(accelCalibrationXOffset) + returnStr)
    uart.write('Y = ' + str(accelCalibrationYOffset) + returnStr)
    uart.write('Z = ' + str(accelCalibrationZOffset) + returnStr)


# Main - wait for user input:

#DisplayFileSystem()

CalibrateAccelerometer()

#while True:
#    if button_a.is_pressed():
        # calibrate
        # setup a new data set
#        break
#    elif button_b.is_pressed():
#        ClearFileSystem()
#    else:
#        display.show("?")

#DisplayStartSequence()


while (sampleMillisTotal <= sampleMillisMax):
    accelData = str(CreateLoggerEntry())
    uart.write(accelData)
    sleep(sampleMillis)
    #with open('data' + str(sampleMillisTotal), 'wb') as my_new_file:
    #    my_new_file.write(accelData)
    sampleMillisTotal = (sampleMillisTotal + sampleMillis)

#todo - file system too small to store locally

#counter = 0
#while (sampleMillisTotal <= sampleMillisMax):
#    accelData = str(CreateLoggerEntry())
#    sleep(sampleMillis)
#    uart.write(accelData)
#    with open('data' + str(sampleMillisTotal), 'w') as my_new_file:
#        my_new_file.write(accelData)
#    sampleMillisTotal = (sampleMillisTotal + sampleMillis)

# SINGLE FILE
#counter = 0
#while (sampleMillisTotal <= sampleMillisMax):
#    accelData = str(CreateLoggerEntry())
#    sleep(sampleMillis)
#    uart.write(accelData)
#    with open(filename, 'w') as my_new_file:
#        my_new_file.write(accelData)
#    sampleMillisTotal = (sampleMillisTotal + sampleMillis)
    
#DisplayEndSequence()
