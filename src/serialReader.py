"""!@file main.py
    This file contains all the funcitons printing out
    a graph of the input from the ADC.
    @author Lucas Sandsor
    @author Jack Barone
    @author Jackson Myers
    @date 8-Feb-2022 
"""
from matplotlib import pyplot
import serial   
def isnum(string):
    '''!@brief Tries to convert a string to a number
        @param string    A string to be converted to a float
        @return    Returns a boolean that is true if the string
        can be converted to a number and false if it cannot
    '''
    try:
        float(string)
        return True
    except ValueError as e:
        return False
    
def serialHandler():
    '''!@brief A program to handle the serial input and output 
        @detail Program handles serial communication and prints
        a nice graph to visualize the signal read by the ADC over time.
        Sends a s for 'serial run', and then sends a c to stop the program
        get the ADC values and time over serial
    '''
    adc_list = []
    with serial.Serial('COM4', 115200) as s_port:
        for line in s_port:
            #manually sent EOF needed because serial port doesn't have EOF
            if b',' in line:
                split_line = line.split(b',')
                for split in split_line:
                    print(split)
                    if b'EOF' in split:
                        pyplot.plot(adc_list)
                        pyplot.grid()
                        pyplot.autumn()
                        pyplot.ylabel("adcValues")
                        pyplot.xlabel("Time")
                        pyplot.show()
                    if isnum(split):
                        adc_list.append(float(split))
     
if __name__ == "__main__":
    #Created serialHandler in case we want to impliment this function later
    serialHandler()