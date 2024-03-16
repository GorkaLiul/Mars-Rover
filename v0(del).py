import serial.tools.list_ports
import serial
ports = serial.tools.list_ports.comports()

ser = serial.Serial()


def CheckBoardPort(ports):
    for i in ports:
        #print(i) #uncoment to list all ports
        boardPort = i
        if "Serie estándar sobre el vínculo Bluetooth (COM3)" in i:
            print(i)


#board = serial.Serial(baundarate = 9600) #boardPort from list (chekc that matches the actual port)
#def writeToCSV(fileName):
#   Csv = open(file = fileName,newline='')#specify separators (newline must be a char)
#   Csv.truncate() #dellete remaining data
CheckBoardPort(ports)
#writeToCSV("Data.csv")

