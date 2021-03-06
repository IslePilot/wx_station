#!/usr/bin/python

"""
Copyright (C) 2015 AeroSys Engineering, Inc.

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
  2015-01-09, ksb, created
"""

import sys
sys.path.append("..")

import time
import datetime
import signal

from __hardware.Adafruit_ADS1x15 import ADS1x15

# define a version for this file
VERSION = "1.0.20150109a"

def signal_handler(signal, frame):
  """This exits cleanly after receiving a control-c"""
  print "You pressed Control-c.  Exiting."
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


class Pyranometer(object):
  # address selections
  ADDR_GND = 0x48
  ADDR_VDD = 0x49
  ADDR_SDA = 0x4a
  ADDR_SCL = 0x4b

  ADS1015 = 0x00	# 12-bit ADC
  ADS1115 = 0x01	# 16-bit ADC

  def __init__(self):
    """Initialize the ADS1115 object."""
    self.adc = ADS1x15(address=Pyranometer.ADDR_GND,
                       ic=Pyranometer.ADS1115)
    return

  def get_readings(self):
    """Read the pyranometer.  This code reads 1 sample at 250 Hz in the
    expectation that a user downstream will be calling this every 0.25 
    seconds and averaging appropriately."""

    # get a timestamp and a reading
    timenow = datetime.datetime.utcnow()
    # set the gain for a maximum of 1.024 V
    volts1 = self.adc.readADCDifferential(chP=0, chN=1, pga=2048, sps=250)/1000.0
    volts2 = self.adc.readADCDifferential(chP=2, chN=3, pga=2048, sps=250)/1000.0
    print "{:.3f} {:.3f}".format(volts1, volts2)

    return volts1, volts2


def main():
  print("Copyright (C) 2015 AeroSys Engineering, Inc.")
  print("This program comes with ABSOLUTELY NO WARRANTY;")
  print("This is free software, and you are welcome to redistribute it")
  print("under certain conditions.  See GNU Public License.")
  print("")

  print("Press Control-c to exit.")

  # instance the anemometer class
  pyranometer = Pyranometer()

  # read the values and loop
  while True:
    # get the readings
    volts, flux = pyranometer.get_readings()

# only run main if this is called directly
if __name__ == '__main__':
  main()

