#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use( "Agg" )
import pylab
import analyzeData as aD
import numpy as np
import sys


def plot( data, rangoX, rangoY, dirname = "." ):
#  interp = [ 'none', 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos' ]
  interp = [ 'none', 'sinc' ]
  aD.plot_parameters()
  for tp in interp:
    fig = pylab.figure( 1, ( 8, 7 ) )
    fig.add_subplot( 111 )
    img = pylab.imshow( data, interpolation = tp, extent = [ min( rangoX ), max( rangoX ), min( rangoY ), max( rangoY ) ], origin = "lower" )
    pylab.colorbar( img, fraction = 0.046, pad = 0.04, format='%.1e' )
    pylab.xlabel( "Position [um]" )
    pylab.ylabel( "Position [um]" )
    pylab.tight_layout()
    pylab.savefig( dirname + "/scan2D_" + "_%s.png" % tp)
    pylab.close()

def readResults():
  pairs = []
  x = []
  y = []
  data_files = []
  fd = open( "scan2D.txt", "r" )
  lines = fd.readlines()
  for i in range( 1, len( lines ) ):
    #if i > 200: continue
    line = lines[ i ].replace( "\n", "" ).split( "\t" )
    data_files.append( line[ 0 ] )
    x.append( int( line[ 1 ] ) )
    y.append( int( line[ 2 ] ) )
    pairs.append( float( line[ 3 ] ) )
  fd.close()
  return data_files, x, y, pairs

def main():
  data = []
  xx = []
  yy = []
  data_files, x, y, pairs = readResults()
  for datax, datay, pair in zip( x, y, pairs ):
    if datax not in xx:
      data.append( [] )
      xx.append( datax )
    if datay not in yy:
      yy.append( datay )
    data[ -1 ].append( pair )
  plot( np.array( data ).T, xx, yy)


if __name__ == "__main__":
  main()
