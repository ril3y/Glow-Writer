#!/usr/bin/env python
import string, os, serial, sys, glob 


class FontWriter(object):
    BANNER = """                                                                                        
    //   ) )                           ||   / |  / /                                    
   //        //  ___                   ||  /  | / /  __     ( ) __  ___  ___      __    
  //  ____  // //   ) ) //  / /  / /   || / /||/ / //  ) ) / /   / /   //___) ) //  ) ) 
 //    / / // //   / / //  / /  / /    ||/ / |  / //      / /   / /   //       //       
((____/ / // ((___/ / ((__( (__/ /     |  /  | / //      / /   / /   ((____   // \n"""
    
    

    
    LEADING_VALUE = "g0x50\n"
    GCODE_FONT_PATH = "../GcodeFonts/RileysFont"
    alphabet = []

    def __init__(self):
        self.generateFontTable()  #populates lookup table for font
        self.GlowWriter = TinygSerial()
        
    def goInteractive(self):
        print self.BANNER
        while(1):
            
            text = raw_input("Input> ")
            if text == "":
                self.GlowWriter.write(self.createGcodeString("\n"))
            elif text == "!!":
                self.GlowWriter.turnOnLaser()
            elif text == "!":
                self.GlowWriter.turnOffLaser()
            elif text == "??":
                self.GlowWriter.zero()
            elif text == ":":
                pass
            elif text == "*":
                self.GlowWriter.goHome()
            else:
                gcode_output = self.createGcodeString(text.upper())
                #print gcode_output
                self.GlowWriter.write(gcode_output)        

    def _getLetter(self, letter):
        for l in self.alphabet:
            if str(l.name) == letter:
                return l


    def createGcodeString(self, string):
        outputGcode = ""
        SPACE = "M5 G90\N G0X20\N"
        
        for i in range(0,len(string)):
            _tmpLetter = string[i]
            if _tmpLetter == " ":
                _tmpLetter = "space"
            elif _tmpLetter == "\n":
                _tmpLetter = "new_line"
            elif _tmpLetter == "@":
                _tmpLetter = "atsign"
            elif _tmpLetter == "/":
                _tmpLetter = "forward_slash"
            elif _tmpLetter == "#":
                _tmpLetter = "pound_sign"

            letter = self._getLetter(_tmpLetter)
            if(letter != None):            
                #print letter
                outputGcode = outputGcode + letter.gcode + SPACE
        return outputGcode
        


    def generateFontTable(self):
        upperLetters = string.uppercase
        lowerLetters = string.lowercase
        specialChars = ["new_line","space", "atsign", "forward_slash", "pound_sign"]
        numbers = range(0,10)


        self.iterateRanges(upperLetters)
        self.iterateRanges(specialChars)
        #We need to put in the lower and special chars font still
        #self.iterateRanges(lowerLetters)
        self.iterateRanges(numbers)



    def iterateRanges(self, charRange):
        for tmpChar in range(0, len(charRange)):
            for f in os.listdir(self.GCODE_FONT_PATH):
                if str(charRange[tmpChar]) == str(f.split(".gcode")[0]):
                    tmpF = open(self.GCODE_FONT_PATH+"/"+f,"r")  
                    gcode = tmpF.read() + self.LEADING_VALUE #THIS IS THE SPACE BETWEEN LETTERS

                    _tmpLetter = Letter(charRange[tmpChar], gcode)
                    self.alphabet.append(_tmpLetter)
                    #print "Found: %s" % _tmpLetter
                    break




class Letter(object):
    def __init__(self, name, gcode):
        self.name = name
        self.gcode = gcode

    def increateFontSize(percentage):
        pass

    def decreaseFontSize(percentage):
        pass

    def __repr__(self):
        return "Letter(name: %s gcode: %s)" % (self.name, (self.gcode).replace("\n"," "))


class TinygSerial(object):
    def __init__(self):
        TRAVEL_REV1 = "$1tr=25000\n"
        TRAVEL_REV2 ="$2tr=25000\n"
        
        tinyg = self.serial_ports()
        if(tinyg):    
            self.glowy = serial.Serial(tinyg,115200,rtscts=1)

        if(not self.glowy.isOpen):
            print("Could not open serial port %s " % tinyg)
            sys.exit(1)
        else:
            #We are open and ready to rock the kitty time.
            print("Serial Port Opened: %s" % self.glowy.portstr)
            
            #scaling
            self.write(TRAVEL_REV1)             
            self.write(TRAVEL_REV2)
            
            
    def turnOnLaser(self):
        self.write("m3\n")
        
    def turnOffLaser(self):
        self.write("m5\n")
        
    def zero(self):
        self.write("G28.3X0Y0\n")
        
    def goHome(self):
        self.write("G90\n g0x0y0\n")
        self.write("G90\n g0x0y0\n")
        self.write("G90\n g0x0y0\n")



    def write(self, string):
        self.glowy.write(string)
        #print("Wrote: %s to Glow Writer" % string)

    def serial_ports(self):
        """Lists serial ports

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of available serial ports
        """
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        for p in result:
            if p.find("usbmodem") != -1:
                return p
            else:
                pass
        return None    







if __name__ == "__main__":
    fw = FontWriter()
    fw.goInteractive()
