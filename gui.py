##MESSAGES FROM THE SEND_MESSAEGS FUNCTION WILL BE INTERPRETED BY THE ARDUINO
    ##MESSAGES FROM THE SEND_MESSAEGS FUNCTION WILL BE INTERPRETED BY THE ARDUINO
    ##MESSAGES FROM THE SEND_MESSAEGS FUNCTION WILL BE INTERPRETED BY THE ARDUINO
    ##MESSAGES FROM THE SEND_MESSAEGS FUNCTION WILL BE INTERPRETED BY THE ARDUINO
    ##MESSAGES FROM THE SEND_MESSAEGS FUNCTION WILL BE INTERPRETED BY THE ARDUINO


from time import sleep
import serial
import serial.tools.list_ports
import csv
import pandas as pd
from tkinter import *
from tkinter import ttk
from math import sin, cos, atan2

def listPorts():
    portsCMP = serial.tools.list_ports.comports()
    return [port.device for port in portsCMP]

def update_joystick(event):
    x = event.x
    y = event.y

    distance = ((x - joystick_center) ** 2 + (y - joystick_center) ** 2) ** 0.5

    if distance > joystick_radius:
        angle = atan2(y - joystick_center, x - joystick_center)
        x = int(joystick_center + joystick_radius * cos(angle))
        y = int(joystick_center + joystick_radius * sin(angle))

    norm_x = round(((x - joystick_center) / joystick_radius) * 100)
    norm_y = round(((joystick_center - y) / joystick_radius) * 100)

    joystick_position["text"] = f"X: {norm_x}, Y: {norm_y}"

    joystick_canvas.coords(dot, x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius)

    send_message()

def reset_cursor_position(event=None):
    x = joystick_center
    y = joystick_center
    joystick_canvas.coords(dot, x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius)
    joystick_position["text"] = "X: 0, Y: 0"

def resetBoard():
    global boardPort
    global board
    boardPort = port_var.get()
    board = serial.Serial(boardPort, 9600)
    board.setDTR(False)
    sleep(2)
    board.flushInput()
    board.setDTR(True)

def ToCsv():
    oFile = open("Data.csv", "w+")
    oFile.truncate()

    maxPoints = 50
    for i in range(maxPoints):
        try:
            dataPoint = board.readline()
            decoded_DataPoint = dataPoint.decode("utf-8").strip('\r\n')

            if i == 0:
                values = decoded_DataPoint.split(",")
            else:
                values = [float(x) for x in decoded_DataPoint.split()]
            print(values)
            text_box.insert(END, decoded_DataPoint + "\n")
            text_box.see(END)
        except:
            print("line missing")

    visualizer = pd.read_csv("Data.csv")
    print(visualizer.head())

def connect():
    resetBoard()
    joystick_canvas.config(state="normal")
    send_button.config(state="normal")

def send_message():
    message = entry.get()
    if 'board' in globals():
        board.write(message.encode())

def export_csv():
    if 'board' in globals():
        board.write("to CSV".encode())
    ToCsv()
def main():
    global port_var
    global text_box
    global board
    global entry
    global joystick_center
    global joystick_radius
    global joystick_position
    global joystick_canvas
    global dot
    global dot_radius
    global send_button
    global face

    ports = listPorts()

    root = Tk()
    root.title("Port Selection")

    port_label = Label(root, text="Select Serial Port:")
    port_label.pack()

    port_var = StringVar(root)
    port_var.set(ports[0])

    port_menu = OptionMenu(root, port_var, *ports)
    port_menu.config(width=20)
    port_menu.pack(pady=10)

    connect_button = Button(root, text="Connect", command=connect, bg="blue", fg="white")
    connect_button.pack(pady=10)

    text_title = Label(root, text="Serial Port Messages:")
    text_title.pack()

    text_frame = Frame(root)
    text_frame.pack(pady=10)

    text_box = Text(text_frame, height=20, width=40)
    text_box.pack(side=LEFT)

    scrollbar = ttk.Scrollbar(text_frame, command=text_box.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_box.config(yscrollcommand=scrollbar.set)

    entry_frame = Frame(root)
    entry_frame.pack(pady=10)

    entry = Entry(entry_frame, width=40)
    entry.pack(side=LEFT)

    send_button = Button(entry_frame, text="Send", command=send_message, state=DISABLED)
    send_button.pack(side=LEFT, padx=5)

    main_frame = Frame(root)
    main_frame.pack()

    joystick_frame = Frame(main_frame)
    joystick_frame.pack(side=RIGHT)

    joystick_canvas = Canvas(joystick_frame, width=200, height=200, bg="white", state=DISABLED)
    joystick_canvas.pack()

    joystick_center = 100
    joystick_radius = 80
    joystick_canvas.create_oval(joystick_center - joystick_radius, joystick_center - joystick_radius,
                                joystick_center + joystick_radius, joystick_center + joystick_radius, outline="black")

    dot_radius = 5
    dot = joystick_canvas.create_oval(joystick_center - dot_radius, joystick_center - dot_radius,
                                      joystick_center + dot_radius, joystick_center + dot_radius, fill="red")

    joystick_canvas.bind("<B1-Motion>", update_joystick)
    joystick_canvas.bind("<ButtonRelease-1>", lambda event: joystick_position.config(text=""))

    joystick_position = Label(root, text="", font=("Arial", 12))
    joystick_position.pack()
    root.bind("<Leave>", reset_cursor_position)
    root.bind("<ButtonRelease-1>", reset_cursor_position)
    root.bind("<ButtonRelease-1>", reset_cursor_position)

    export_button = Button(root, text="Export CSV", command=export_csv)
    export_button.pack(pady=10)
    face = joystick_canvas.create_oval(0, 0, 0, 0, outline="red", fill="red")

    root.mainloop()

if __name__ == "__main__":
    main()

print("success")
