'''!
@file main.py
    Creates an interrupt service routine to read data from ADC. Outputs a signal to an external RC circuit then reads the resulting signal.
    The data can then be read with the serialReader class.
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

micropython.alloc_emergency_exception_buf(100)
q0 = task_share.Queue ('h', 1000,name = "Queue Interrupt")

def callback1(t):
    #print("Print inside of interrupt")
    q0.put(adcpin.read(),in_ISR=True)


if __name__ == "__main__":
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
    
        