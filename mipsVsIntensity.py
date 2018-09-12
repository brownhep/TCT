# -*- coding: utf-8 -*-

import os
import numpy as np
from OOFlex.interface.InterfaceFactory import InterfaceFactory
from OOFlex.files.BINReader import BINReader
import math
import pylab
from scipy import optimize
import scipy.special as sp
from matplotlib.patches import Ellipse
from analyzeData import *

def cut( x, y ):
  for i in range( len( x )-1, -1, -1 ):
    if x[ i ] < -1.6:
      del x[ i ]
      del y[ i ]
  return x, y  

def plot( x, y ):
  fig = pylab.figure( 1, ( 6, 4 ) )
  fig.add_subplot( 111 )
  pylab.plot( x, y, "ko", fillstyle = "none" )
  xx = np.linspace( min( x ), max( x ), num = 100 )
  x, y, = cut( x, y )
  m, b = np.polyfit( x, y, 1 )
  pylab.plot( xx, m * xx + b, "k-", label = "Linear fit" )
#  pylab.xticks( np.arange( min( x ), max( x ), 0.2 ) )
#  pylab.yticks( range( 0, 1000, 100 ) )
  pylab.xlabel( "Waveform Minimum (V)" )
  pylab.ylabel( "MIPs" )
  xticks = list( pylab.xticks()[ 0 ] )
  yticks = list( pylab.yticks()[ 0 ] )
  stepy = yticks[ 1 ] - yticks[ 0 ]
  if b < 0:
    pylab.text( xticks[ 1 ], yticks[ 1 ], "y=%.2f*x%.2f" %( m,b ) )
  else:  
    pylab.text( xticks[ 1 ], yticks[ 1 ], "y=%.2f*x+%.2f" %( m,b ) )  
  pylab.text( xticks[ 1 ], yticks[ 0 ] + stepy/2, "MIPS=100, Height=%.2f(V)" %( ( 100 - b )/m ) )  
  pylab.grid( True )
  pylab.tight_layout()
  pylab.savefig( "mipsVsHeight.png" )
  pylab.close()

def plot2( x, y ):
  fig = pylab.figure( 2, ( 6, 4 ) )
  fig.add_subplot( 111 )
  pylab.plot( x, y, "ko", fillstyle = "none" )
  xx = np.linspace( min( x ), max( x ), num = 100 )
  x, y, = cut( x, y )
  m, b = np.polyfit( x, y, 1 )
  pylab.plot( xx, m * xx + b, "k-", label = "Linear fit" )
#  pylab.xticks( np.arange( min( x ), max( x ), 0.2 ) )
#  pylab.yticks( range( 0, 1000, 100 ) )
  pylab.xlabel( "Intensity (%)" )
  pylab.ylabel( "MIPs" )
  xticks = list( pylab.xticks()[ 0 ] )
  yticks = list( pylab.yticks()[ 0 ] )
  stepy = yticks[ 1 ] - yticks[ 0 ]
  if b < 0:
    pylab.text( xticks[ 1 ], yticks[ 1 ], "y=%.2f*x%.2f" %( m,b ) )
  else:  
    pylab.text( xticks[ 1 ], yticks[ 1 ], "y=%.2f*x+%.2f" %( m,b ) )  
  pylab.text( xticks[ 1 ], yticks[ 0 ] + stepy/2, "MIPS=100, Intensity=%.2f(%%)" %( ( 100 - b )/m ) )  
  pylab.grid( True )
  pylab.tight_layout()
  pylab.savefig( "mipsVsIntensity.png" )
  pylab.close()

def readResults():
  mips = []
  height = []
  data_files = []
  intensities = []
  if not os.path.exists( "mipsVsIntensity.txt" ):
    return data_files, height, intensities, mips    
  fd = open( "mipsVsIntensity.txt", "r" )
  lines = fd.readlines()
  for i in range( 1, len( lines ) ):
    line = lines[ i ].replace( "\n", "" ).split( "\t" )
    data_files.append( line[ 0 ] )
    height.append( float( line[ 1 ] ) )
    mips.append( float( line[ 3 ] ) )
    intensities.append( float( line[ 2 ] ) )
  fd.close()  
  return data_files, height, intensities, mips

def writeResults( data_files, height, intensities, mips ):
  fd = open( "mipsVsIntensity.txt", "w" )
  fd.write( "File\tHeight[V]\tIntensity[%%]\tMips\n" )
  for i in range( len( mips ) ):
    fd.write( data_files[ i ] + "\t" + str( height[ i ] ) + "\t" + str( intensities[ i ] ) + "\t" + str( mips[ i ] ) + "\n" )
  fd.close()

def parseador():  #To convert the timestamp to a normal date time: datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  parser = argparse.ArgumentParser( description = "MIPs vs Laser Intensity" )
  parser.add_argument( "-b", "--bulk", type = str, choices = [ "p", "n" ], required = True, help = "bulk of the sensor. Choices = n, p", metavar = "" )
  parser.add_argument( "-f", "--files", nargs="+", type = str, help = "data files to process.", metavar = "" )
  args = parser.parse_args()
  return args

def main():
  args = parseador()  
  data_files, height, intensities, mips = readResults()
  for filename in args.files:
    if filename not in data_files: 
      intensities.append( float( filename.split( "_")[ 3 ].replace( "I", "" ) ) )
      header, data = getData( filename )
      charge, cvdata, cutteddata, avWaveform = processData( filename, data, header, args )
      pairs, integral = strmResults( charge )
      data_files.append( filename )  
      mips.append( integral )
      height.append( min( avWaveform ) )
  writeResults( data_files, height, intensities, mips )    
  plot_parameters()  
#  plot( height, mips )
  plot2( intensities, mips )

if __name__ == "__main__":
  main()  

