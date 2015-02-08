#!/usr/bin/python
from random import randint, uniform
from decimal import Decimal
#random file

xmax = 800
ymax = 800


shotmax = 30
TWOPLACES = Decimal(10) ** -4
f = open("shotout.nc", "w")
f.writelines("G0x0y0\n")

distant_stars = (0.01,.05)
near_stars = (.6, .1)
close_stars = (.1,.15)
small_moon = (1,2)
large_moon = (4,6)


def shoot_field(_file, star_field_type, number_of_stars):
    for x in range(0,number_of_stars):     
        delay = Decimal(uniform(star_field_type[0], star_field_type[1])).quantize(TWOPLACES)
        shot_sequence = """(Shot #%d) N%d\ng0x%sy%s\n M3\n g4p%s\n M5\n""" % (x,x,randint(0,xmax), randint(0,ymax), delay)
        _file.write(shot_sequence)
        print(shot_sequence)

shoot_field(f, distant_stars, 50)
shoot_field(f, near_stars, 15)
shoot_field(f, close_stars, 3)
shoot_field(f, small_moon,3)
shoot_field(f, large_moon,1)


f.close()


print "done shooting"