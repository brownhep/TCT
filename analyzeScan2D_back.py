#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import analyzeData as aD
from TCTData import TCTData
import coordinatesFile as cF
import shutil

def processAndAnalysis( filename, count, args, cut = "signal" ):
  noiseFile = "electronicNoise.bin"
  noiseTCT = TCTData( noiseFile )
  noiseTCT.bulk = args.bulk
  dataTCT = TCTData( filename )
  dataTCT.bulk = args.bulk
  aD.getData( noiseTCT )
  aD.getData( dataTCT )
  aD.convertAndShiftData( noiseTCT )
  charge = aD.processData( dataTCT, noiseTCT, args.verbosity, cut )
  pairs, mips = aD.strmResults( charge )
  if (args.verbosity or count % 100 == 0):
    print "Charge: %eC" % charge
    print "Pairs: %d" % pairs
    print "MIPs (300um): %.2f" % mips
  return pairs

def readResults():
  pairs = []
  x = []
  y = []
  data_files = []
  if not os.path.exists( "scan2D.txt" ):
    return data_files, x, y, pairs
  fd = open( "scan2D.txt", "r" )
  lines = fd.readlines()
  for i in range( 1, len( lines ) ):
    line = lines[ i ].replace( "\n", "" ).split( "\t" )
    data_files.append( line[ 0 ] )
    x.append( int( line[ 1 ] ) )
    y.append( int( line[ 2 ] ) )
    pairs.append( float( line[ 3 ] ) )
  fd.close()
  return data_files, x, y, pairs

def writeResults( data_files, x, y, pairs ):
  fd = open( "scan2D.txt", "w" )
  fd.write( "File\tx(um)\ty(um)\tPairs\n" )
  for i in range( len( pairs ) ):
    fd.write( "%s\t%d\t%d\t%f\n" % ( data_files[ i ], x[ i ], y[ i ], pairs[ i ] ) )
  fd.close()

def maximumCoordinates( x, y, pairs ):
  indexMax = pairs.index( max( pairs ) )
  maxx = x[ indexMax ]
  maxy = y[ indexMax ]
  return maxx, maxy

def writeNewCoord( newx, newy, detector ):
  shutil.copyfile( "sensors.txt", "sensors_back.txt" )
  sensors = cF.getCoordFromFile()
  newCoord = sensors[ detector ]
  newCoord[ 0 ] = newx
  newCoord[ 1 ] = newy
  X, Y, Z = newCoord
  if detector == "Ref":
    cF.changeRelCoordRefDiode( X, Y, Z )
    print "New Coord, sensor %s: %s %s %s" % ( detector, X, Y, Z )
    return
  sensors = cF.changeCoordinate( sensors, detector, X, Y, Z )
  sensors = cF.setCoordHoldSyst( sensors )
  cF.writeCoord2File( sensors )
  print "New Coord, sensor %s: %s %s %s" % ( detector, X, Y, Z )

def natSorting( dataFiles ):
  data = {}
  files = []
  for filename in dataFiles:
    coord = filename.replace( ".bin", "" ).split( "_" )[ 2: ]
    x = int( coord[ 0 ][ 1 : ] )
    y = int( coord[ 1 ][ 1 : ] )
    if x not in data.keys():
      data[ x ] = {}
    data[ x ][ y ] = filename
  for key in sorted( data.keys() ):
    for key2 in sorted( data[ key ].keys() ):
      files.append( data[ key ][key2 ] )
  return files

def parseador():
  parser = argparse.ArgumentParser( description = "Scan2D analyzer" )
  parser.add_argument( "-b", "--bulk", type = str, required = True, choices = [ "p", "n" ], help = "bulk of the sensor. Choices = n, p", metavar = "" )
  parser.add_argument( "-v", "--verbosity", type = int, required = False, default = 1, help = "Verbosity, plots for individual scans are produced only when the verbosity is on. Choices = 0, 1", metavar = "" )
  args = parser.parse_args()
  return args

def main( args ):
  data_files, x, y, pairs = readResults()
  nTotFiles = len([ fd for fd in os.listdir( "." ) if "scan2D" in fd and ".bin" in fd ])
  count = 0
  for filename in natSorting( [ fd for fd in os.listdir( "." ) if "scan2D" in fd and ".bin" in fd ] ):
    if filename not in data_files:
      if (args.verbosity or count % 100 == 0):
        print "Finished analyzing", count, "/", nTotFiles, "files"
        print "Filename: %s" % filename
      coord = filename.replace( ".bin", "" ).split( "_" )[ 2: ]
      data_files.append( filename )
      x.append( int( coord[ 0 ][ 1 : ] ) )
      y.append( int( coord[ 1 ][ 1 : ] ) )
      pairs.append( processAndAnalysis( filename, count, args ) )
      count = count + 1
  writeResults( data_files, x, y, pairs )
  maxx, maxy = maximumCoordinates( x, y, pairs )
  writeNewCoord( maxx, maxy, data_files[ 0 ].split( "_" )[ 1 ] )


if __name__ == "__main__":
  args = parseador()
  main( args )
