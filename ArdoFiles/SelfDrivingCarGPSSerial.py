import serial

#ser = serial.Serial('COM3', baudrate = 115200, timeout = 1)
ser = serial.Serial(2, 115200)
i = 0

def parseData(data):
    if(ord(data[0]) >= 48 and ord(data[0])<= 57):
            arr = data.split(' ')
            if(len(arr) < 3):
                return arr[0]
            return arr

while 1:
        #ser.write(bytes(1))
        #ser.write('drive')
        ardoData = ser.readline()
        ardoData = ardoData.decode(encoding='UTF-8',errors='replace')
        data = parseData(ardoData)
        if(data != None):
                print(data)

        
