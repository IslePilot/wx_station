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
  2015-01-01, ksb, created
"""

import sys
sys.path.append("..")

import time
import datetime
import signal

# define a version for this file
VERSION = "1.0.20150101a"

def signal_handler(signal, frame):
  print "You pressed Control-c.  Exiting."
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



def main():
  print("Copyright (C) 2015 AeroSys Engineering, Inc.")
  print("This program comes with ABSOLUTELY NO WARRANTY;")
  print("This is free software, and you are welcome to redistribute it")
  print("under certain conditions.  See GNU Public License.")
  print("")

  print("Press Control-c to exit.")


# only run main if this is called directly
if __name__ == '__main__':
  main()
