#!/usr/bin/env python

import time



app_key = "YOURKEY"
app_secret = "YOURSECRET"
oauth_token = "YOUR TOKEN" #
oauth_token_secret = "YOUR SECRET TOKEN" #

from twython import Twython
from twython import TwythonStreamer
from TextToGcode import FontWriter

#twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret) # Setup a Twython object



class TweetStreamer(TwythonStreamer):
    fw = FontWriter()
    fw.GlowWriter.goHome()
    
    linecount = 0
    MAX_LINE_COUNT  = 12
    MAX_LINE_LEN = 28
        
    def on_success(self, data):
        if 'text' in data:
            
            if self.linecount  >= self.MAX_LINE_COUNT:
                self.fw.GlowWriter.goHome()
                self.linecount = 0
                
            text = data['text']
    
            text = text.upper()
            temp_text = text
            text = ""
            while len(temp_text) > self.MAX_LINE_LEN:
                text += temp_text[:self.MAX_LINE_LEN] + "\n"
                self.linecount = self.linecount + 1
                temp_text = temp_text[self.MAX_LINE_LEN:]
            text += temp_text
                
                
            print("Printing Tweet: " + text)
            self.fw.GlowWriter.write(self.fw.createGcodeString(text))
            self.fw.GlowWriter.write(self.fw.createGcodeString("\n"))
            self.linecount = self.linecount + 1
          
                            
    def on_error(self, status_code, data):
        print status_code
        self.disconnect()
        
    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)
    
def streamed():
    while True:
        try:
            streamer = TweetStreamer(app_key, app_secret, oauth_token, oauth_token_secret)
            #streamer.statuses.filter(track = '#NYE', stall_warnings=True)
            streamer.statuses.filter(track = '#glowwriter', stall_warnings=True)
        except Exception, e:
            print e.message

streamed()
