#/usr/bin/python2

"""
Copyright (C) 2017 AeroSys Engineering, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Revision History:
    2017-09-17: ksb, created in support of weather station creation.  Used existing fence_station.py as a starting point
"""

# define a version for this file
VERSION = "1.0.20170917a"


import time
import datetime
import signal

import am2315 as am
import bmp180 as bmp
import rainwise111 as rain

class FenceStationData():
    def __init__(self):
        # Sensor: AM2315 - Temperature and Humidity Sensor
        # http://www.aosong.com/asp_bin/Products/en/AM2315.pdf
        temperature_f = None
        temperature_c = None
        relative_humidity_pct = None
        
        # Sensor: BMP180 - Digital Pressure Sensor
        # https://cdn-shop.adafruit.com/datasheets/BST-BMP180-DS000-09.pdf
        
        
        
        return


def signal_handler(signal, frame):
    """Called by the signal handler when Control C is pressed"""
    print "Fence_Station.py:  You pressed Ctrl-c.  Exiting."
    # set the flag to terminate the rain gauge monitoring thread, and wait for it to close
    rain.RAINWISE_TERMINATE_REQUEST = True
    time.sleep(1.0)
    
    # exit cleanly
    sys.exit(0)

# trap Control C presses and call the signal handler
signal.signal(signal.SIGINT, signal_handler)

def main():
    # add the GPL license output
    print("Copyright (C) 2017 AeroSys Engineering, Inc.")
    print("This program comes with ABSOLUTELY NO WARRANTY;")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions.  See GNU Public License.")
    print("")
    print"Version: ", VERSION
    
    # start here
    am2315 = am.AM2315()
    bmp180 = bmp.BMP180(sensor_elevation_ft = 5089.0)
    rain111 = rain.Rainwise111()
    total_rain_in = 0.0
    
    # the first two readings of the AM2315 might be junk, read and skip
    t_f, t_c, rh = am2315.get_readings()
    time.sleep(1)
    t_f, t_c, rh = am2315.get_readings()
    time.sleep(1)
    
    # main loop
    while True:
        # read the data
        # Read the AM2315
        t2315_f, t2315_c, rh2315 = am2315.get_readings()
        
        # Read the BMP180
        t180_f, t180_c, p180_inhg, slp180_inhg, pa180_ft = bmp180.get_readings()
        
        # Read the Rain Gauge
        interval_rain_in = rain111.get_readings()
        total_rain_in = total_rain_in + interval_rain_in
        
        # compute the density altitude
        da_ft = bmp.compute_density_altitude(p180_inhg, t2315_f)
        
        # get the CPU temp
        t_cpu_c = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
        t_cpu_f = t_cpu_c * 9.0/5.0 + 32.0
        
        # get a timestamp
        timenow = datetime.datetime.utcnow()
        str_time = timenow.strftime("%Y-%m-%d %H:%M:%S")
        
        # show the user what we got
        print
        print "{:s}:".format(str_time)
        print "Temperature(F):{:.2f} Humidity(%):{:.1f} ".format(t2315_f, rh2315)
        print "Pressure(inHg):{:.2f} Sea-Level Pressure(inHg):{:.2f}".format(p180_inhg, slp180_inhg)
        print "Pressure Altitude:{:.1f} Density Altitude:{:.1f}".format(pa180_ft, da_ft)
        print "New Rain:{:.2f} Total Rain:{:.2f}".format(interval_rain_in, total_rain_in)
        print "CPU Temp:{:.2f} Board Temp:{:.2f}".format(t_cpu_f, t180_f)
        
        time.sleep(5)

# only run main if this is called directly
if __name__ == '__main__':
    main()

