import numpy as np
import serial
import visa

class Lakeshore_224:
    '''Module to readout Lakeshore 224 module
    '''
    def __init__(self):
        '''Open the serial port
        '''
        self.ser = serial.Serial(port='com3', baudrate=57600, bytesize=7, parity=serial.PARITY_ODD)
    
    def read_chs(self, ch_str='a'):
        '''Query LakeShore with the input as the channel as a string, 
        say '0' (reading out all channels, 'a' (reading out channel A)
        Return: array of the temperature in Kelvin from specified channels
        '''
        self.ser.write('krdg? %s\r\n'%ch_str)
        output = self.ser.readline()
        output = np.array(output.split(','))
        output = output.astype(np.float)
        return output 
    
    def close(self):
        '''Close the serial port
        '''
        self.ser.close()
        
class Agilent_E3647a_PS:
    '''Module to operate Agilent_E3647a power supply
    '''
    def __init__(self, gpib_address=1):
        self.device = visa.ResourceManager().open_resource('GPIB0::%d::INSTR'%gpib_address)
        self.device.write('OUTP ON')
        
    def set_voltage(self, volt, ch):
        '''Set voltage (V) of the channel
        volt gives the voltage to be set
        ch gives the output chanel
        '''
        self.device.write('INST OUT%d'%ch)
        self.device.write('APPLY %f, MAX'%(volt))
    
    def set_current(self, curr, ch):
        '''Set current (A) of the channel
        curr gives the current to be set
        ch gives the output chanel
        '''
        self.device.write('INST OUT%d'%ch)
        self.device.write('APPLY MAX, %f'%(curr))
        
    def meas_voltage(self, ch):
        '''Measuring the voltage (V) via remote sensing from 
        the rear terminals
        ch gives the output chanel
        '''
        self.device.write('INST OUT%d'%ch)
        return float(self.device.query('MEAS:VOLT?'))
    
    def meas_current(self, ch):
        '''Measuring the current (A)
        ch gives the output chanel
        '''
        self.device.write('INST OUT%d'%ch)
        return float(self.device.query('MEAS:CURR?'))    
    
    def close(self):
        '''Close the device'''
        self.device.write('INST OUT1')
        self.device.write('APPLY MIN, MIN')
        self.device.write('INST OUT2')
        self.device.write('APPLY MIN, MIN')
        self.device.write('OUTP OFF')
        self.device.close()
