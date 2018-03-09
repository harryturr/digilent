'''
8 March 2018
Working code, loop iteration properly configured for set number of pulses

'''
from ctypes import *
from dwfconstants import *
import time
import sys

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hzFreq = 5e4 #Wave frequency
cSamples = 4096
#declare ctype variables
hdwf = c_int()
rgdSamples = (c_double*cSamples)()
channel = c_int(0)

# samples between -1 and +1
for i in range(0,len(rgdSamples)):
    rgdSamples[i] = 1.0*i/cSamples;

#print DWF version
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print "DWF Version: "+version.value

#open device
"Opening first device..."
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print "failed to open device"
    quit()

#__________________________________________________________________________
  
print "Generating custom waveform..."

#Setting up the parameters for waveform    
#print "Generating custom waveform..."
dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, funcCustom) #Define custom waveform; funcCustom
dwf.FDwfAnalogOutNodeDataSet(hdwf, channel, AnalogOutNodeCarrier, rgdSamples, c_int(cSamples))  
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(hzFreq)) #Set frequency attribute in Hz
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(4.0)) #Set amplitude attribute in Volts

dwf.FDwfAnalogOutRunSet(hdwf, channel, c_double(1/hzFreq)) # run for 1 periods
dwf.FDwfAnalogOutWaitSet(hdwf, channel, c_double(1 / hzFreq)) # wait one pulse time 
dwf.FDwfAnalogOutRepeatSet(hdwf, channel, c_int(1)) # repeat 1 times 

pulses = 5
for j in range(1,pulses + 1):
    
    #print 'Generating pulse in:'
    for k in range(1, 4):
        #print 4-k
        time.sleep(k)
    print j
  
    dwf.FDwfAnalogOutConfigure(hdwf, channel, c_bool(True)) # starts the waveform
    time.sleep(1)   
    
print "done."
dwf.FDwfDeviceCloseAll() 
