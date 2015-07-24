#/usr/bin/python2

"""
Copyright (C) 2014 AeroSys Engineering, Inc.

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
  2014-12-31, ksb, created
"""

import sys
sys.path.append("..")

import time
import datetime
import signal

import am2315 as am
import bmp180 as bmp
import rainwise111 as rain

# define a version for this file
VERSION = "1.0.20150724a"

def signal_handler(signal, frame):
  print "Fence_Station.py:  You pressed Ctrl-c.  Exiting."
  rain.RAINWISE_TERMINATE_REQUEST = True
  time.sleep(1.0)
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
  # add the GPL license output
  print("Copyright (C) 2014 AeroSys Engineering, Inc.")
  print("This program comes with ABSOLUTELY NO WARRANTY;")
  print("This is free software, and you are welcome to redistribute it")
  print("under certain conditions.  See GNU Public License.")
  print("")

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
    t_f, t_c, p_inhg, slp_inhg, pa_ft, da_ft = bmp180.get_readings()

    # get a timestamp
    timenow = datetime.datetime.utcnow()
    str_time = timenow.strftime("%Y-%m-%d %H:%M:%S")

    # show the user what we got
    print "{:s}: T(F):{:.2f} T(C):{:.2f} P(inHg):{:.2f} SLP(inHg):{:.2f} PA(ft):{:.1f} DA:{:.1f}".format(str_time,
                                                                                                            t_f,
                                                                                                            t_c,
                                                                                                            p_inhg,
                                                                                                            slp_inhg,
                                                                                                            pa_ft,
                                                                                                            da_ft)


    # we only want to read the AM2315 and Rain every 5 seconds
    if timenow.second%5 == 0:
      t_f, t_c, rh = am2315.get_readings()
    
      str_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
      print("{:s}: T(F):{:.2f} T(C):{:.2f} RH:{:.1f}".format(str_time, t_f, t_c, rh))

      interval_rain_in = rain111.get_readings()
      total_rain_in = total_rain_in + interval_rain_in

      print("{:s}: New Rain:{:.2f} Total Rain:{:.2f}".format(str_time, interval_rain_in, total_rain_in))

    time.sleep(1)

# only run main if this is called directly
if __name__ == '__main__':
  main()

