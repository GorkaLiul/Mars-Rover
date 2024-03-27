# Mars-Rover


#0: Project Aim
This program aims to create an interface to control and reconfigure a rover in which technologies such as **Arduino** will be implemented. 

#1. HOW DOES IT WORK?

**Board connection** and **GUI** have been developed using  *python*, whereas *C++* and **.Ino** files have been used to control the physical components of the project. 

#1.1 MOVEMENT & CONTROL: 

Although its not even by far finished, data storage to scv files has been made, aiming to fully control the rover arduino code will be carefully developed to work hand by hand with the GUI application. We expect to implement analogical controls such as joysticks(Digital from the gui or physical ) to control it and additional buttons to fulfill different functionalities.

#1.2.0 GUI, DIGITAL CONTROL & DATA ANALYSIS: 

For the sake of the project we've decided a GUI interface is essential for this project to be open to anyone with non to bassic coding knowledge, this commes to the issue of having to make a bi-directional control system from the arduino to the user interface because the need to create do design and additional code which sum up to be an excessive amount of time. 

The design is being created with Figma and tkinter using Tkinter-Designer: check link to see rep: https://github.com/ParthJadhav/Tkinter-Designer

![img.png](Desription Images (Ignore)/Current GUI.png)
The design is clearly missing of any aesthetic due to tight deadlines, hopefully action will be taken on this silly nonsense later. :/           


#1.2.1 DATA ANALYSIS: 

for different functions such as scanning the surroundings and ploting, all the data sent by the serial port will be stored and a csv file, which will be structured as data tables using pandas, to different analysis operations such as plotting. 
all the plots will be made using the Matplotlib library which provides a huge variety of prebuilt plotting systems. 

![MatplotLib.png](Desription%20Images%20%28Ignore%29%2FMatplotLib.png)