'''!
@file main.py
    This file contains the callback for the Lab 4 interrupt and the main function.
	Main initializes the ADC, then gets values from it in a loop. Values are added to the queue from the ADC via an ISR.
@author Lucas Sandsor
@author Jack Barone
@author Jack Meyers
@date 8-Feb-2022
'''

import gc
import pyb
import cotask
import task_share
import motorDriver
import encoderDriver
import controls
import utime
import micropython

'''!
Allot 100 bytes of memory for an unforeseen exception buffer
'''
micropython.alloc_emergency_exception_buf(100)


'''!
Create a global queue for the interrupt to use to share values
with the main function
'''
q0 = task_share.Queue ('h', 1000,name = "Queue Interrupt")

def callback1(t):
    '''!
    @brief Interrupt subroutine
    @detail Callback1 is interrupt subroutine function that is passed
    to a timer to be used. It reads the adcpin and puts the
    read value into a queue to be printed
    '''
    q0.put(adcpin.read(),in_ISR=True)


if __name__ == "__main__":
    # Initialize the ADC and the circuit input pin.
	adcValues = []
    pinc0 = pyb.Pin (pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
    pinc1 = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    adcpin = pyb.ADC(pinc0)
    tim1 = pyb.Timer(1, freq=250)
    
    while(1):
        #pyb.enable_irq()
        tim1.callback(callback1)
        pinc1.high()
        utime.sleep_ms(2000)
        pinc1.low()
        utime.sleep_ms(2000)
        #pyb.disable_irq()
        tim1.callback(None)
        while(q0.empty() is False):
            num = q0.get()
            print(num, end=b',')
            adcValues.append(num)
        adcValues = []
        print(b'EOF')
    
        