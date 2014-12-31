#!/usr/bin/env python
import string, os, serial, sys, glob 


class FontWriter(object):
    BANNER = """                                                                                        
    //   ) )                           ||   / |  / /                                    
   //        //  ___                   ||  /  | / /  __     ( ) __  ___  ___      __    
  //  ____  // //   ) ) //  / /  / /   || / /||/ / //  ) ) / /   / /   //___) ) //  ) ) 
 //    / / // //   / / //  / /  / /    ||/ / |  / //      / /   / /   //       //       
((____/ / // ((___/ / ((__( (__/ /     |  /  | / //      / /   / /   ((____   // \n"""
    
    

    
    
    GCODE_FONT_PATH = "../GcodeFonts/RileysFont"
    alphabet = []

    def __init__(self):
        self.generateFontTable()  #populates lookup table for font
        self.GlowWriter = TinygSerial()
        print self.BANNER
        while(1):
            
            text = raw_input("Input> ")
            if text == "":
                self.GlowWriter.write(self.createGcodeString("\n"))
            elif text == "!!":
                self.GlowWriter.turnOnLaser()
            elif text == "!":
                self.GlowWriter.turnOffLaser()
            elif text == "0":
                self.GlowWriter.zero()
            elif text == "*":
                self.GlowWriter.goHome()
            else:
                gcode_output = self.createGcodeString(text)
                #print gcode_output
                self.GlowWriter.write(gcode_output)
            

    def _getLetter(self, letter):
        for l in self.alphabet:
            if l.name == letter:
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

            letter = self._getLetter(_tmpLetter)
            #print letter
            outputGcode = outputGcode + letter.gcode + SPACE
        return outputGcode
        


    def generateFontTable(self):
        upperLetters = string.uppercase
        lowerLetters = string.lowercase
        specialChars = ["new_line","space"]
        numbers = range(0,9)


        self.iterateRanges(upperLetters)
        self.iterateRanges(specialChars)
        #We need to put in the lower and special chars font still
        #self.iterateRanges(lowerLetters)
        #self.iterateRanges(numbers)



    def iterateRanges(self, charRange):
        for tmpChar in range(0, len(charRange)):
            for f in os.listdir(self.GCODE_FONT_PATH):
                if charRange[tmpChar] == f.split(".gcode")[0]:
                    tmpF = open(self.GCODE_FONT_PATH+"/"+f,"r")  
                    gcode = tmpF.read()

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
        tinyg = self.serial_ports()
        if(tinyg):    
            self.glowy = serial.Serial(tinyg,115200,rtscts=1)

        if(not self.glowy.isOpen):
            print("Could not open serial port %s " % tinyg)
            sys.exit(1)
        else:
            #We are open and ready to rock the kitty time.
            print("Serial Port Opened: %s" % self.glowy.portstr)
            
    def turnOnLaser(self):
        self.write("m3\n")
        
    def turnOffLaser(self):
        self.write("m5\n")
        
    def zero(self):
        self.write("G28.3X0Y0\n")
        
    def goHome(self):
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
