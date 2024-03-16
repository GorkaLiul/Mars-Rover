import tkinter as tk

# Function to get the text from the textbox
def get_text():
    text = entry.get()
    print("Text entered:", text)

# Create the main window
window = tk.Tk()

# Set the title of the window
window.title("Mars Rover")

# Set the dimensions of the window
window.geometry("800x500")

# Create a textbox (Entry widget)
entry = tk.Entry(window)
entry.pack(pady=20)  # Adding some padding

# Create a button to get the text from the textbox
button = tk.Button(window, text="Send Serial Message ", command=get_text)
button.pack()

# Start the Tkinter event loop
window.mainloop()