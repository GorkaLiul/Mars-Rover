from serial.tools import list_ports
import serial
import time
def scvdell():
    oFile = open("Data.csv", "w+")# w+ extension to open the file in write mode --> pulls error
    oFile.truncate()

def listPorts():
    portsCMP = serial.tools.list_ports.comports()
    for port in portsCMP:
        print(port)

def resetBoard():

    boardPort = input("board port: COMx?: ")
    board = serial.Serial(boardPort, 9600)
    board.setDTR(False)
    time.sleep(2)
    board.flushInput()
    board.setDTR(True)


    #  Board reset uncomplete yet
def main():
    listPorts()
    scvdell()
    resetBoard()

main()
print("success")

