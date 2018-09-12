#!/usr/bin/env python
# -*- coding: utf-8 -*-

from OOHw.interface.InterfaceFactory import InterfaceFactory
import powerSupply as pW
import argparse

def main( args ):
  factory = InterfaceFactory( "setupBrown.ini" )
  keithley = factory.getDevice( "highVoltage" )
  print keithley.readVoltage()
  print keithley.readCurrent()
  pW.setPowerSupply( keithley, args.voltage, args.compliance )

def parseador():  # To convert the timestamp to a normal date time: datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  parser = argparse.ArgumentParser( description = "TCT acquisition program with Lecroy Lc725Zi" )
  parser.add_argument( "-v", "--voltage", type = str, default = "0", help = "bias voltage applied to the sensor in V. Default = %(default)sV", metavar = ""  )
  parser.add_argument( "-m", "--compliance", type = float, default = "1e-3", help = "compliance high voltage power supply. Default = %(default)sA", metavar = "" )
  parser.add_argument( "-b", "--bulk", type = str, choices = [ "p", "n" ], default = "n", help = "bulk of the sensor. Choices = n, p. Default = %(default)s", metavar = "" )
  args = parser.parse_args()
  if float( args.voltage  ) > 0 and args.bulk == "n":
    parser.error( "n bulk requires negative voltage" )
  if float( args.voltage  ) < 0 and args.bulk == "p":
    parser.error( "p bulk requires positive voltage" )

  args = parser.parse_args()
  return args

if __name__ == "__main__":
  args = parseador()
  main( args )
