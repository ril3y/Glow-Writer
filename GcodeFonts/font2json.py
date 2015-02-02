#!/usr/bin/env python


import os
import fnmatch
import simplejson as json

outfile = open("alphanumeric.json", "w")


all = {
  "fontName":"RileysFont",
  "alphabet":[ ]
}



for root, dir, files in os.walk("./RileysFont"):
  print root
  print ""
  for items in fnmatch.filter(files, "*.gcode"):
    f = open("./RileysFont/"+items, "r")
    
    if len(items) > 8: #this is a symbol filename
      _name = items.split(".")[0] #remove the .gcode
    else: 
      _name = items[0]
      
    i = {'name':_name,'gcode' :f.read()}
    
    f.close()    
    #print json.dumps(i)
    #outfile.writelines(json.dumps(i))
    all["alphabet"].append(i)
outfile.close()


jsonOut = {
  "font_name":"RileysFont",
  "characters":[]
}

for l in all["alphabet"]:
  _tmpChar = json.dumps(l)
  jsonOut['characters'].append(l)
print(jsonOut)
f = open("RileysFont.json","w")
f.write(json.dumps(jsonOut))
f.close()


  
