from microbit import *
import os
import array

#todo no globals please
sampleMillis = 500
sampleMillisTotal = 0
sampleMillisMax = 1000 * 10000
filename = 'data.csv'
displayStartSequenceMillis = 300
displayEndSequenceMillis = 200
returnStr = '\r\n'
accCalXOffset = 0
accCalYOffset = 0
accCalZOffset = 0


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


# Converts accelerometer sensor reading to m/sec2
def MilliGToMSec(x):
    convertedValue = x / (1000 * 9.8)
    return convertedValue

# Log accel array
def LogSampledAccelData(accelData):
    uart.write(str(accelData[0]) + ',' + str(accelData[1]) + ',' + str(accelData[2]) + ',' + str(accelData[3]) +  returnStr)
        
    #TODO remove outliers
    #Returns Sampled Accelerometer data 
def GetSampledAccelData(accCalOffsets):
    maxTime = 100
    sampleTime = 5
    currentTime = 0
    currentCount = 0
    sampleArray = array.array('d',[0.0,0.0,0.0])
    
    xDataList = []
    yDataList = []
    zDataList = []
    
    while (currentTime < maxTime):
        
        xDataList.append(MilliGToMSec(accelerometer.get_x()) - accCalOffsets[0])
        yDataList.append(MilliGToMSec(accelerometer.get_y()) - accCalOffsets[1])
        zDataList.append(MilliGToMSec(accelerometer.get_z()) - accCalOffsets[2])
        
        sleep(sampleTime)
        currentTime = currentTime + sampleTime
        currentCount = (currentCount + 1)
        
    #TODO fix this lazy outlier filtering
    
    xDataList.sort()
    xDataList.pop()
    xDataList.pop(0)
    for dataEntry in xDataList:
        sampleArray[0] = sampleArray[0] + dataEntry
    
    yDataList.sort()
    yDataList.pop()
    yDataList.pop(0)
    for dataEntry in yDataList:
        sampleArray[1] = sampleArray[1] + dataEntry
    
    zDataList.sort()
    zDataList.pop()
    zDataList.pop(0)
    for dataEntry in zDataList:
        sampleArray[2] = sampleArray[2] + dataEntry    
    
    returnArray = array.array('d',[running_time(),0.0,0.0,0.0])
    
    returnArray[1] = sampleArray[0] / (currentCount - 2)
    returnArray[2] = sampleArray[1] / (currentCount - 2)
    returnArray[3] = sampleArray[2] / (currentCount - 2)
    
    LogSampledAccelData(returnArray)
    return returnArray
    
# Returns an array of X,Y,Z calibration offsets in m/sec2
# Args calibrateMillisMax is total sample period
def CalibrateAccelerometer(calibrateMillisMax):
    calibrateMillisTotal = 0
    calibrateMillis = 1
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

    accCalXOffset = MilliGToMSec(xSum / calibrationCounter)
    accCalYOffset = MilliGToMSec(ySum / calibrationCounter)
    accCalZOffset = MilliGToMSec(zSum / calibrationCounter)

    uart.write('Accelerometer Calibrated' + returnStr)
    uart.write('X = ' + str(accCalXOffset) + returnStr)
    uart.write('Y = ' + str(accCalYOffset) + returnStr)
    uart.write('Z = ' + str(accCalZOffset) + returnStr)
    return array.array('d',[accCalXOffset,accCalYOffset,accCalZOffset])

#----------------------------------------------------
#                       MAIN
#----------------------------------------------------

# DisplayFileSystem()





# Calibrate Accelerometer (over a period of 5 secs)
accelCalibrationArray = CalibrateAccelerometer(5000)

# Sample loop
while (True):
    GetSampledAccelData(accelCalibrationArray)






while (True):
    accelData = str(CreateLoggerEntry())
    uart.write(accelData)
    sleep(sampleMillis)
    #with open('data' + str(sampleMillisTotal), 'wb') as my_new_file:
    #    my_new_file.write(accelData)
    sampleMillisTotal = (sampleMillisTotal + sampleMillis)


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
