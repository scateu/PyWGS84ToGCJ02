from pynmea import nmea
import serial
import os
from WGS84ToGCJ02 import transform

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

ser = serial.Serial("COM2",38400)
while True:
    line = ser.readline()
    if(line[4] == 'G'): # $GPGGA
        if(len(line) > 50):
            #print line
            gpgga = nmea.GPGGA()
            gpgga.parse(line)
            lats = gpgga.latitude
            longs = gpgga.longitude
            
            #convert degrees,decimal minutes to decimal degrees 
            _lat = (float(lats[2]+lats[3]+lats[4]+lats[5]+lats[6]+lats[7]+lats[8]))/60
            lat = (float(lats[0]+lats[1])+_lat)
            _long = (float(longs[3]+longs[4]+longs[5]+longs[6]+longs[7]+longs[8]+longs[9]))/60
            longs = (float(longs[0]+longs[1]+longs[2])+_long)
            
            #calc position
            pos_y = lat
            pos_x = -longs #longitude is negaitve

    #import code
    #code.interact(local=locals())
    #cls()
        #print "Lat: %s  Long: %s    Alt: %s    Sats: %s"%(gpgga.latitude,gpgga.longitude,gpgga.antenna_altitude,gpgga.num_sats)
        print "WGS84:",lat,longs #WGS84
        print "GCJ02:",transform(lat,longs) #GCJ02
    
