'''!
@file motorDriver.py
File contains the necessary code to enable and run a motor using PWM.
Pin numbers and timer are parameterized so multiple motors can be run at the same time.
@author Lucas Sandsor
@author Jack Barone
@author Jack Meyers
@date 11-Jan-2022
'''

import pyb
class MotorDriver:
    '''!
    This class impliments a motor driver for ME405
    '''
    def __init__ (self, en_pin, in1pin, in2pin, timer):
        '''!
        Creates a motor driver by initializing GPIO
        pins and turning motor on and off
        @param en_pin    The pin to enable movement for the motor
        @param in1pin    Input pin 1 for driving the motor forwards
        @param in2pin    Input pin 2 for driving the motor backwards 
        @param timer    The numierc value for the timer on the STM32
        that works in PWM mode that allows us to supply a duty cycle
        to the motor via PWM signal
        '''
        #print("Creating a motor driver")
        self.pinEN = pyb.Pin (en_pin, pyb.Pin.OUT_PP)
        self.pinIN1 = pyb.Pin (in1pin, pyb.Pin.OUT_PP)
        self.pinIN2 = pyb.Pin (in2pin, pyb.Pin.OUT_PP)
        #must declare pyb.Pin.board.en_pin in main
        self.tim = pyb.Timer (timer, freq=20000)
        self.ch1 = self.tim.channel (1, pyb.Timer.PWM, pin=self.pinIN1)
        self.ch2 = self.tim.channel (2, pyb.Timer.PWM, pin=self.pinIN2)
        
        
    def set_duty_cycle(self, level):
        '''!
        This method sets duty cycle of motor to a certain
        level. Positive cuase torque in one direction and
        negative causes torque in another.If the duty cycle is out of
        the acceptable range, it will go to the closest value
        it can (100 if 105 is given)
        @param level    The duty cycle level to run the motor at (-100 to 100)
        '''
        if(level > 100):
            #print ('Setting duty cycle to ' + str (100))
            self.ch2.pulse_width_percent (0)
            self.ch1.pulse_width_percent (100)
        elif(level < -100):
            #print ('Setting duty cycle to ' + str (-100))
            self.ch2.pulse_width_percent (100)
            self.ch1.pulse_width_percent (0)
        else:
            #print ('Setting duty cycle to ' + str (level))
            self.pinEN.value(255)
            if(level > 0):
                self.ch2.pulse_width_percent (0)
                self.ch1.pulse_width_percent (abs(level))
            else:
                self.ch1.pulse_width_percent (0)
                self.ch2.pulse_width_percent (abs(level))
