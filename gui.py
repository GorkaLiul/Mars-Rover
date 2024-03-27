import serial
import serial.tools.list_ports
import csv
import pandas as pd
from tkinter import *
from time import sleep

def list_ports():
    portsCMP = serial.tools.list_ports.comports()
    return [port.device for port in portsCMP]


def reset_board(board_port):
    global board
    board = serial.Serial(board_port, 9600)
    board.setDTR(False)
    sleep(2)
    board.flushInput()
    board.setDTR(True)


def to_csv():
    with open("Data.csv", "w+") as oFile:
        oFile.truncate()
        max_points = 50
        for i in range(max_points):
            try:
                data_point = board.readline()
                decoded_data_point = data_point.decode("utf-8").strip('\r\n')

                if i == 0:
                    values = decoded_data_point.split(",")
                else:
                    values = [float(x) for x in decoded_data_point.split()]
                print(values)
                text_box.insert(END, decoded_data_point + "\n")  # Insert received message into Text widget
                text_box.see(END)  # Scroll to the end of the Text widget
            except:
                print("line missing")  # Except to not throw an error

            writer = csv.writer(oFile, delimiter=',')  # separator between elements
            writer.writerow(values)

    visualizer = pd.read_csv("Data.csv")
    print(visualizer.head())


def connect():
    selected_port = port_var.get()
    reset_board(selected_port)
    to_csv()


def main():
    global port_var
    global text_box
    global board

    ports = list_ports()

    root = Tk()
    root.title("Port Selection")

    port_label = Label(root, text="Select Serial Port:")
    port_label.pack()

    port_var = StringVar(root)
    port_var.set(ports[0])  # default value

    port_menu = OptionMenu(root, port_var, *ports)
    port_menu.config(width=20)
    port_menu.pack(pady=10)

    connect_button = Button(root, text="Connect", command=connect, bg="blue", fg="white")
    connect_button.pack(pady=10)

    # Create a Text widget for displaying received messages
    text_box = Text(root, height=20, width=50)
    text_box.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()

print("success")
