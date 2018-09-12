# -*- coding: utf-8 -*-

import socket
import time


def open_socket():
  ip_address = "128.148.63.202"
  port = 5020
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect( ( ip_address, port ) )
  return s

def close_socket( s ):
  s.send( "Q\r\n" )
  s.close()

def getRelativeCoordinates( s ):
  s.send("W0\r\n")
  X = int( s.recv( 1024 ).split( "." )[ 0 ] )
  s.send("W1\r\n")
  Y = int( s.recv( 1024 ).split( "." )[ 0 ] )
  s.send("W2\r\n")
  Z = int( s.recv( 1024 ).split( "." )[ 0 ] )
  return [ str( X ), str( Y ), str( Z ) ]

def getAbsoluteCoordinates( s ):
  s.send( "R0\r\n" )
  X = int( s.recv( 1024 ).split( "." )[ 0 ] )
  s.send( "R1\r\n" )
  Y = int( s.recv( 1024 ).split( "." )[ 0 ] )
  s.send( "R2\r\n" )
  Z = int( s.recv( 1024 ).split( "." )[ 0 ] )
  return [ str( X ), str( Y ), str( Z ) ]

def sendtoCoordinates( s, coordinates ):
  it = 0
  coordinates = map( str, coordinates )
  while True:
    print "Sending the laser to:", coordinates
    s.send( "A0M" + coordinates[ 0 ] + "\r\n" )
    x = str( int( s.recv( 1024 ).replace( "\r\n", "" ) ) )
    s.send( "A1M" + coordinates[ 1 ] + "\r\n" )
    y = str( int( s.recv( 1024 ).replace( "\r\n", "" ) ) )
    s.send( "A2M" + coordinates[ 2 ] + "\r\n" )
    z = str( int( s.recv( 1024 ).replace( "\r\n", "" ) ) )
    print "Current coordinates: %s %s %s" % ( x, y, z )
    if x == coordinates[ 0 ] and y == coordinates[ 1 ] and z == coordinates[ 2 ]:
      break
    elif it == 10:
      print "Reached the end of the stage."
      return [ "out", "out", "out" ]
    else:
      it += 1
      time.sleep( 0.1 )

def enableLimitSwitch (s, enable):
  if enable == 0:
    s.send("D\r\n")
    x = s.recv( 1024 ).replace( "\r\n", "" )
  else:
    s.send("E\r\n")
    x = s.recv( 1024 ).replace( "\r\n", "" )
  print x
  return x


if __name__ == "__main__":
  pass
