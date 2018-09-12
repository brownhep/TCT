#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab
import sys
#import analyzeData as aD


def readResults( filename ):
  voltage = []
  current = []
  fd = open( filename, "r" )
  lines = fd.readlines()
  fd.close()
  for line in lines:
    data = line.split( "\t" )
    voltage.append( abs( float( data[ 0 ] ) ) )
    current.append( abs( float( data[ 1 ] ) * 1e3 ) )
  return voltage, current

def plot( filename, voltage, current ):
#  aD.plot_parameters()
  fig = pylab.figure( 1, ( 7, 6 ) )
  fig.add_subplot( 111 )
  pylab.semilogy( voltage, current, label = "_".join( filename.split( "_" )[ 1 : 3 ] ) )
  pylab.xlabel( "Absolute Voltage [V]" )
  pylab.ylabel( "Absolute Current [mA]" )
  pylab.grid( True )
  pylab.legend( loc = 0 )
  pylab.tight_layout()
  pylab.savefig( "iv_%s.png" % filename.split( "_" )[ 1 ] )

def main( files ):
  for filename in files:
    voltage, current = readResults( filename )
    plot( filename, voltage, current )


if __name__ == "__main__":
  main( sys.argv[ 1 : ] )
