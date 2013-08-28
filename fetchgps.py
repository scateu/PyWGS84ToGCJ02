from pynmea import nmea
import serial
import os
from WGS84ToGCJ02 import transform
from WGS84Distance import distance

#import threading

#class ThreadWorker(threading.Thread):
    #def __init__(self, callable, *args, **kwargs):
        #super(ThreadWorker, self).__init__()
        #self.callable = callable
        #self.args = args
        #self.kwargs = kwargs

    #def run(self):
        #self.callable(*self.args, **self.kwargs)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def decodeNMEAStream(serialport,GCJ02=False):
    while True:
        line = serialport.readline()
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

            if GCJ02:
                return transform(lat,longs)
            else:
                return (lat,longs)

if __name__ == "__main__":
    ser = serial.Serial("COM2",38400)

    origin_position = ()
    current_position = ()

    origin_position = decodeNMEAStream(ser,GCJ02=True)
    while True:
        current_position = decodeNMEAStream(ser,GCJ02=True)
        print current_position,
        print "distance:",distance(origin_position,current_position)*1000,'m'
