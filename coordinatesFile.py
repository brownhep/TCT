# -*- coding: utf-8 -*-

import numpy as np
import datetime


def readFileCoordinates():
  fd = open( "sensors.txt" )
  lines = fd.readlines()
  fd.close()
  return lines

def writeFileCoordinates( lines ):
  fd = open( "sensors.txt", "w" )
  fd.writelines( lines )
  fd.close()

def readOriginPos():
  fd = open( "Stage_origin.txt" )
  lines = fd.readlines()
  print lines
  originAry = lines[ 3 ].replace( "\n", "" ).split( " " )[0:3]
  print originAry
  origin = [ int( value ) for value in originAry ]
  print "Origin: ", origin
  fd.close()
  return origin

def writeOriginPos( origin ):
  fd = open( "Stage_origin.txt", "w" )
  lines = []
  lines.append(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + "\n")
  lines.append( "#Origin position in relative coordiantes\n" )
  lines.append( "x y z\n" )
  for i in xrange(3): lines.append( str(origin[i]) + " " )
  lines.append( "\n" )
  fd.writelines( lines )
  fd.close()

def getCoordFromFile():
  """Coordinates are returned in the stages relative system.
  """
  sensors = { "First" : [], "Second" : [], "Third" : [], "Fourth": [], "Fifth" : [], "Sixth" : [], "Seventh": [], "Ref" : [] }
  lines = readFileCoordinates()
  sensors[ "absCoordRefDiode" ] = [ int( value ) for value in lines[ 2 ].split( " " ) ]
  sensors[ "relCoordRefDiode" ] = [ int( value ) for value in lines[ 5 ].split( " " ) ]
  keys = lines[ 9 ].replace( "\n", "" ).split( " " )
  for i in range( 3 ):
    line = np.array( [ int( value ) for value in lines[ 10 + i ].split( " " ) ] ) + sensors[ "relCoordRefDiode" ][ i ]
    for j in range( len( line ) ):
      sensors[ keys[ j ] ].append( line[ j ] )
  return sensors

def writeCoord2File( sensors ):
  keys = [ "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Ref" ]
  lines = []
  lines.append( "#Absolute coordiantes of the reference diode\n" )
  lines.append( "x y z\n" )
  lines.append( " ".join( map( str, sensors[ "absCoordRefDiode" ]  ) ) + "\n" )
  lines.append( "#Relative coordiantes of the reference diode\n" )
  lines.append( "x y z\n" )
  lines.append( " ".join( map( str, sensors[ "relCoordRefDiode" ]  ) ) + "\n" )
  lines.append( "#Relative coordinates of the sensors to the reference diode\n" )
  lines.append( "#First line sensor names, second line x-coordinate\n" )
  lines.append( "#third line y-coordinate, fourth line z-coordinate\n" )
  lines.append( " ".join( keys ) + "\n" )
  for i in range( 3 ):
    coord = []
    for key in keys:
      coord.append( sensors[ key ][ i ] )
    lines.append( " ".join( map( str, coord ) ) + "\n" )
  writeFileCoordinates( lines )

def setCoordHoldSyst( sensors ):
  keys = [ value for value in sensors if value != "relCoordRefDiode" ]
  for key in keys:
    for i in range( 3 ):
      sensors[ key ][ i ] = sensors[ key ][ i ] - sensors[ "relCoordRefDiode" ][ i ]
  return sensors

def changeCoordinate( sensors, detector, X, Y, Z ):
#  if detector == "Ref":
#    sensors = changeRelCoordRefDiode( sensors, X, Y, Z )
  sensors[ detector ] = [ int( X ), int( Y ), int( Z ) ]
  return sensors

def changeRelCoordRefDiode( X, Y, Z ):
  lines = readFileCoordinates()
  lines[ 5 ] = "%s %s %s\n " % ( X, Y, Z )
  writeFileCoordinates( lines )

def changeAbsCoordRefDiode( X, Y, Z ):
  lines = readFileCoordinates()
  lines[ 2 ] = "%s %s %s\n " % ( X, Y, Z )
  writeFileCoordinates( lines )

def getRelPosRef( sensors ):
  origin = readOriginPos()
  absPos = sensors["absRefPosition"]

#def changeRelCoordRefDiode( sensors, X, Y, Z ):
#  sensors[ "relCoordRefDiode" ] = [ int( X ), int( Y ), int( Z ) ]
#  return sensors


if __name__ == "__main__":
  pass
