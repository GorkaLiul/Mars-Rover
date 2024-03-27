from serial.tools import list_ports
import serial
from time import sleep
import csv
import pandas as pd


def listPorts():
    portsCMP = serial.tools.list_ports.comports()
    for port in portsCMP:
        print(port)


def resetBoard():

    global boardPort
    global board
    boardPort=  input("board port: COMx?: ")
    board = serial.Serial(boardPort, 9600)
    board.setDTR(False)
    sleep(2)
    board.flushInput()
    board.setDTR(True)

def ToCsv():
    oFile = open("Data.csv", "w+")# w+ extension to open the file in write mode --> pulls error
    oFile.truncate()

    maxPoints = 50
    for i in range(maxPoints):
        try:
            dataPoint = board.readline()
            decoded_DataPoint = dataPoint.decode("utf-8").strip('\r\n')

            if i == 0:
                values = decoded_DataPoint.split(",")
            else:
                values = [float(x) for x  in decoded_DataPoint.split()]
            print(values)
        except:
             print("line missing")#Except to not throw an error

        writer = csv.writer(oFile, delimiter=',')#separator between elements
        writer.writerow(values)
    oFile.close()

    visualizer = pd.read_csv("Data.csv")
    print(visualizer.head())



def main():
    global oFile
    listPorts()
    resetBoard()
    ToCsv()

main()

print("success")
