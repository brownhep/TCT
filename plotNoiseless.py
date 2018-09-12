# -*- coding: utf-8 -*-

import os.path
import argparse
import numpy as np
import pylab
import analyzeData as aD
from TCTData import TCTData


class noiselessTCTData( TCTData ):
  def __init__( self, filename ):
    super( noiselessTCTData, self ).__init__( filename )
    self.__noiselessData = []
    self.__voltage = self.__setVoltage()

  @property
  def noiselessData( self ):
    return self.__noiselessData

  @noiselessData.setter
  def noiselessData( self, value ):
    self.__noiselessData = value

  @property
  def voltage( self ):
    return self.__voltage

  def __setVoltage( self ):
    return [ value[ 1 : ] for value in self.filename.split( "_" ) if value[ 0 ] == "V" and value[ -1 ] == "V" ][ 0 ]

def plotdata( noiselessData ):
  aD.plot_parameters()
  fig = pylab.figure( 1, ( 7, 5 ) )
  fig.add_subplot( 111 )
  for noiseless in noiselessData:
    pylab.plot( noiseless.noiselessData, label = noiseless.voltage )
  pylab.ticklabel_format( style = 'sci', scilimits = ( 0, 0 ) )
  pylab.xlabel( "Time [s]" )
  pylab.ylabel( "Voltage [V]" )
  pylab.legend( loc = 4, ncol = 5 )
  pylab.grid()
  pylab.tight_layout()
  pylab.show()

def plotResults( results ):
  fig = pylab.figure( 20, ( 7, 5 ) )
  fig.add_subplot( 111 )
  pylab.plot( results[ "Voltage" ], results[ "MIPs" ], "ko", fillstyle = "none" )
  pylab.ticklabel_format( axis = "x", style = 'sci', scilimits = ( -1, 4 ) )
  pylab.ticklabel_format( axis = "y", style = 'sci', scilimits = ( 0, 2 ) )
  pylab.ylabel( "MIPs" )
  pylab.xlabel( "Voltage [V]" )
  pylab.legend( loc = 4, ncol = 5 )
  pylab.grid()
  pylab.tight_layout()
  pylab.savefig( "mipsVsVoltage.png" )
  pylab.close()

def fillResults( results, filename, mips, charge ):
  voltage = [ value for value in filename.split( "_") if value[ 0 ] == "V" and value[ -1 ] == "V" ][ 0 ]
  results[ "Files" ].append( filename )
  results[ "Voltage" ].append( voltage[ 1 : -1 ] )
  results[ "MIPs" ].append( mips )
  results[ "Charge" ].append( charge )
  return results

def writeResults( results ):
  if not os.path.exists( "results.txt" ):
    fd = open( "results.txt", "w" )
    fd.write( "File\tVoltage\tCharge\tMIPs\n" )
    fd.close()
  fd = open( "results.txt", "a" )
  for i in range( len( results[ "Files" ] ) ):
    fd.write( results[ "Files" ][ i ] + "\t" + results[ "Voltage" ][ i ] + "\t" + str( results[ "Charge" ][ i ] ) + "\t" + str( results[ "MIPs" ][ i ] ) + "\n" )
  fd.close()

def natSorting( files ):
  indexes = {}
  sorted_files = []
  index = files[ 0 ].split( "_" ).index( [ value for value in files[ 0 ].split( "_" ) if value[ 0 ] == "V" and value[ -1 ] == "V" ][ 0 ] )
  for fd in files:
      indexes[ abs( int( fd.split( "_" )[ index ][ 1 : -1 ] ) ) ] = fd
  for key in sorted( indexes ):
    sorted_files.append( indexes[ key ] )
  return sorted_files

def parseador():
  parser = argparse.ArgumentParser( description = "Plotter of TCT data files." )
  parser.add_argument( "-f", "--files", nargs = "+", help = "data files to process.", metavar = "" )
  parser.add_argument( "-n", "--noise_file", type = str, help = "noise data file to remove from the signal files.", metavar = "" )
  parser.add_argument( "-b", "--bulk", type = str, choices = [ "n", "p" ], required = True, help = "bulk of the sensor to analyze.", metavar = "" )
  parser.add_argument( "-i", "--integration_window", type = str, choices = [ "signal", "peak", "whole" ], default = "signal", help = "definiton of the integration window, 50ns since the beginning of the peak or only the peak. Choices = signal, peak. Default = signal.", metavar = "" )
  args = parser.parse_args()
  return args

def main( files, noise, bulk, integrationWindow ):
#  results = { "Files" : [], "Voltage" : [], "Charge" : [], "MIPs" : [] }
  noiselessDataTCT = []
  noiseTCT = TCTData( noise )
  aD.getData( noiseTCT )
  noiseTCT.bulk = bulk
  aD.convertAndShiftData( noiseTCT )
  for filename in natSorting( files ):
    print "File: %s" % filename
    noiselessDataTCT.append( noiselessTCTData( filename ) )
    noiselessDataTCT[ -1 ].bulk = bulk
    aD.getData( noiselessDataTCT[ -1 ] )
    aD.convertAndShiftData( noiselessDataTCT[ -1 ] )
    noiselessDataTCT[ -1 ].noiselessData = list( np.array( noiselessDataTCT[ -1 ].ydata[ -1 ] ) - np.array( noiseTCT.ydata[ -1 ] ) )

#    header[ "Voltage" ] = [ value[ 1: ] for value in filename.split( "_" ) if value[ 0 ] == "V" and value[ -1 ] == "V" ][ 0 ]
#    for i in range( len( data ) ):
#      charge, cvdata, cutteddata, avWaveform, initCut, endCut, initSignal, endSignal, xdata = processData( filename, data, header, bulk, cut = integrationWindow )
#      pairs, mips = strmResults( charge )
#      results = fillResults( results, filename, mips, charge )
  plotdata( noiselessDataTCT )
#  plotResults( results )
#  writeResults( results )

if __name__ == "__main__":
  args = parseador()
  main( args.files, args.noise_file, args.bulk, args.integration_window )
