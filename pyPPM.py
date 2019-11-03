# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 19:32:25 2019

@author: pyMrak
"""


from sounddevice import OutputStream
from numpy import array, ones, zeros


class PPMgenerator(object):
    
    LOW_DUR = 0.5 #low pulse duration (in milliseconds)
    PCK_DUR = 22.5 #package duration (in milliseconds)
    ST_PAUSE = 1.5 #package start pause (in milliseconds)
    CH_MID = 1.5 #channel mid position (in milliseconds)
    MAX_CH = 8 #maximum nr of output channels 
    
    
    def __init__(self, RCchannelsUsed=4, initialSignal=None,
                 outFreq=200000, device=0):
        
        self.outputFreq = outFreq
        
       # self.callback_status = sd.CallbackFlags()
        
        
        self.multiplier = self.outputFreq/1e3
        self.zeroPulse = int(self.LOW_DUR*self.multiplier)
        self.blockSize = int(self.PCK_DUR*self.multiplier)
        if RCchannelsUsed > self.MAX_CH:
            self.RCchUsed = self.MAX_CH
        else:
            self.RCchUsed = RCchannelsUsed
        if initialSignal:
            self.setChannels(initialSignal)
        else:
            self.setChannels(zeros(RCchannelsUsed))
        self.signalChanged = False
        self.stream = OutputStream(device=device,
                   samplerate=self.outputFreq, 
                   blocksize=self.blockSize,
                   dtype='float32', 
                   channels=1, callback=self._callback)
        
    def _callback(self, outdata, frames, time, status):
        #self.callback_status |= status
        if self.signalChanged:
            outdata[:] = self.signal[:, None]
            self.signalChanged = False
        
    def setChannels(self, channelValues):
        self.channels = array(channelValues[:self.RCchUsed], dtype='float32')
        self.signal = ones(self.blockSize, dtype='float32')
        start = int(self.ST_PAUSE*self.multiplier)
        for i, chVal in enumerate(self.channels):
            chDur = int((chVal/2+self.CH_MID)*self.multiplier)
            self.signal[start:start+self.zeroPulse] = zeros(self.zeroPulse)
            start += chDur
        chDur = int(self.multiplier)
        for j in range(self.MAX_CH-i):
            self.signal[start:start+self.zeroPulse] = zeros(self.zeroPulse)
            start += chDur
        self.signal[start:start+self.zeroPulse] = zeros(self.zeroPulse)   
        self.signalChanged = True
            
    def start(self):
        self.stream.start()
        
    def stop(self):
        self.stream.stop()

    
