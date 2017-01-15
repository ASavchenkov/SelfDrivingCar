import serial

ser = serial.Serial(2, 9600)

while 1:
        for i in range(0,90):
                command = 'f' + str(i);
                ser.write(bytearray(command + 'q', 'utf-8'))
                data = ser.readline()
                #print(data)
                print(data.decode('ascii','replace'))
        

        
