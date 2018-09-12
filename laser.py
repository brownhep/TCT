# -*- coding: utf-8 -*-

import argparse
import socket
import time

def open_socket():
  ip_address = "128.148.63.193"
  port = 5020
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect( ( ip_address, port ) )
  return s

def close_socket( s ):
  s.send( "Q\r\n" )

def turn_laser_off( s ):
  s.send( "X-off\r\n" )
  temp = s.recv( 1024 ).replace( "\r\n", "" )
  return temp

def set_laser_frequency( s, freq ):
  s.send( "X-f " + freq + "\r\n" )
  temp = s.recv( 1024 ).replace( "\r\n", "" )
  return temp

def set_laser_pulse( s, width ):
  s.send( "X-p " + width + "\r\n" )
  temp = s.recv( 1024 ).replace( "\r\n", "" )
  return temp

def get_laser_temperature( s ):
  s.send( "X-s\r\n" )
  temp = s.recv( 1024 ).replace( "\r\n", "" )
  return temp  

def parseador():
  parser = argparse.ArgumentParser( description = "Laser control program" )
  parser.add_argument( "-f", "--frequency", type = str, help = "set the frequency in Hz. Choices = [ 50,..., 500000].", metavar = "")
  parser.add_argument( "-p", "--pulse_width", type = str, help = "set the pulse width in mV. Choices = [330, ..., 3300].", metavar = "" )
  parser.add_argument( "-t", "--temperature", action = "store_true", help = "read the laser temperature"  )
  parser.add_argument( "-o", "--off", action="store_true", help = "turn off the laser")
  args = parser.parse_args()
  if args.pulse_width:
    if int( args.pulse_width ) < 330 or int( args.pulse_width ) > 3300:
      parser.error( "laser.py: error: argument -p/--pulse_width: invalid choice: '%s' (choose from '330', ..., '3300')" % args.pulse_width )
  if args.frequency:    
    if int( args.frequency ) < 50 or int( args.frequency ) > 50000:
      parser.error( "laser.py: error: argument -f/--frequency: invalid choice: '%s' (choose from '50', ..., '50000')" % args.frequency )    
  return args

if __name__ == "__main__":
  args = parseador()
  s = open_socket()
  if args.off:
    temp = turn_laser_off( s )
    print temp
    close_socket( s )
    raise SystemExit
  elif args.temperature:
    turn_laser_off( s )
    time.sleep( 2 )
    temp = get_laser_temperature( s )
    print temp
    close_socket( s )
    raise SystemExit
  elif args.frequency:
    temp = set_laser_frequency( s, args.frequency )  
    print temp
    close_socket( s )
    raise SystemExit
  elif args.pulse_width:
    temp = set_laser_pulse( s, args.pulse_width )
    print temp
    close_socket( s )
    raise SystemExit


