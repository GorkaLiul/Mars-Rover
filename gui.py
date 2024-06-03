from time import sleep
import serial
import serial.tools.list_ports
import csv
import pandas as pd
from tkinter import *
from tkinter import ttk
from math import sin, cos, atan2

# OBJECTS:


def listPorts():
    portsCMP = serial.tools.list_ports.comports()
    return [(port.device, port.description) for port in portsCMP]


def update_joystick(event):
    global norm_x, norm_y
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
    sendData(norm_x, norm_y)
    send_message(norm_x, norm_y)


def reset_cursor_position(event=None):
    global output
    reset_message = "Reset cursor position"
    reset_message_bytes = reset_message.encode() + b'\n'
    if 'board' in globals():
        board.write(reset_message_bytes)
    x = joystick_center
    y = joystick_center
    joystick_canvas.coords(dot, x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius)
    joystick_position["text"] = "X: 0, Y: 0"
    print(f"to {0,0}")
    send_message(0, 0)  # Reset x and y coordinates in the output
    output[0] = 0
    output[1] = 0
    output[2] = 0
    print(output)
def resetBoard():
    global boardPort
    global board
    boardPort = port_var.get()[:5].upper()  # Only store COMx
    board = serial.Serial(boardPort, 9600)
    board.setDTR(False)
    sleep(2)
    board.flushInput()
    board.setDTR(True)


def sendData(x=None, y=None):
    if x and y is None:
        x = 0
        y = 0
    global s1, s2, s3, s4, output
    print(x, y, s1.get(), s2.get(), s3.get(), s4.get(), '\n')
    output = [x, y, s1.get(), s2.get(), s3.get(), s4.get()]

    return None
    # raise NotImplementedError


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


def send_message(x=None, y=None):
    global s1, s2, s3, s4
    global output
    if x and y == None:
        x = 0
        y = 0

    output = [x, y, s1.get(), s2.get(), s3.get(), s4.get()]

    if 'board' in globals():
        # Convert the output to bytes before sending
        output_bytes = ','.join(map(str, output)).encode() + b'\n'
        board.write(output_bytes)

        # Display the sent message in the text box
        text_box.insert(END, f"Sent: {output}\n")
        text_box.see(END)


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
    global sliders_frame
    global s1, s2, s3, s4  # Define s1, s2, s3, s4 here

    ports = listPorts()

    root = Tk()
    root.title("Port Selection")

    port_label = Label(root, text="Select Serial Port:")
    port_label.pack()

    port_var = StringVar(root)
    port_var.set(ports[0][0])  # Selecting the first port by default

    port_menu = OptionMenu(root, port_var, *[f"{port[0]} - {port[1]}" for port in ports])
    port_menu.config(width=50, bg="lightblue")
    port_menu.pack(pady=5)

    connect_button = Button(root, text="Connect", command=connect)
    connect_button.pack(pady=5)

    text_title = Label(root, text="Serial Port Messages:")
    text_title.pack()

    text_frame = Frame(root)
    text_frame.pack(pady=5)

    text_box = Text(text_frame, height=15, width=40)
    text_box.pack(side=LEFT)

    scrollbar = ttk.Scrollbar(text_frame, command=text_box.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_box.config(yscrollcommand=scrollbar.set)

    entry_frame = Frame(root)
    entry_frame.pack(pady=5)

    entry = Entry(entry_frame, width=40)
    entry.pack(side=LEFT)

    send_button = Button(entry_frame, text="Send", command=send_message, state=DISABLED)
    send_button.pack(side=LEFT, padx=5)

    main_frame = Frame(root)
    main_frame.pack()

    joystick_frame = Frame(main_frame)
    joystick_frame.pack(side=LEFT)

    joystick_canvas = Canvas(joystick_frame, width=150, height=150, bg="white", state="normal")
    joystick_canvas.pack()

    joystick_center = 75
    joystick_radius = 60
    joystick_canvas.create_oval(joystick_center - joystick_radius, joystick_center - joystick_radius,
                                joystick_center + joystick_radius, joystick_center + joystick_radius, outline="black")

    dot_radius = 3
    dot = joystick_canvas.create_oval(joystick_center - dot_radius, joystick_center - dot_radius,
                                      joystick_center + dot_radius, joystick_center + dot_radius, fill="red")

    joystick_canvas.bind("<B1-Motion>", update_joystick)
    joystick_canvas.bind("<ButtonRelease-1>", lambda event: reset_cursor_position(), send_message)


    joystick_position = Label(root, text="", font=("Arial", 10))
    joystick_position.pack()
    root.bind("<Leave>", reset_cursor_position)
    root.bind("<ButtonRelease-1>", reset_cursor_position)
    root.title("Rvr")
    export_button = Button(root, text="Export CSV", command=export_csv)
    export_button.pack(pady=5)
    face = joystick_canvas.create_oval(0, 0, 0, 0, outline="red", fill="red")

    sliders_frame = Frame(main_frame)
    sliders_frame.pack(pady=5, padx=10, side=RIGHT)

    s1 = Scale(sliders_frame, from_=180, to=0, orient=VERTICAL, length=150, bg="lightblue", command=send_message)
    s1.pack(side=LEFT, padx=5)
    s1_label = Label(sliders_frame, text="S1")
    s1_label.pack(side=LEFT)

    s2 = Scale(sliders_frame, from_=180, to=0, orient=VERTICAL, length=150, bg="OliveDrab2", command=send_message)
    s2.pack(side=LEFT, padx=5)
    s2_label = Label(sliders_frame, text="S2")
    s2_label.pack(side=LEFT)

    s3 = Scale(sliders_frame, from_=180, to=0, orient=VERTICAL, length=150, bg="salmon1", command=send_message)
    s3.pack(side=LEFT, padx=5)
    s3_label = Label(sliders_frame, text="S3")
    s3_label.pack(side=LEFT)

    s4 = Scale(sliders_frame, from_=180, to=0, orient=VERTICAL, length=150, bg="MediumOrchid1", command=send_message)
    s4.pack(side=LEFT, padx=5)
    s4_label = Label(sliders_frame, text="S4")
    s4_label.pack(side=LEFT)

    root.mainloop()


if __name__ == "__main__":
    main()
