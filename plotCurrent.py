#!/usr/bin/env python
# -*- coding: utf-8 -*-

from OOFlex.files.BINReader import BINReader
from TCTData import TCTData

import math
import argparse
import numpy as np
import matplotlib
matplotlib.use( "Agg" )
import pylab
import os.path


def plot_parameters( plots = 0 ):
  """Plot format
  """
  pylab.rcParams[ 'lines.linewidth' ] = 1
  pylab.rcParams[ 'lines.markeredgewidth' ] = 1
  pylab.rcParams[ 'lines.markersize' ] = 7
  pylab.rcParams[ 'font.size' ] = 10 - plots / 2
#  pylab.rcParams[ 'font.weight' ] = 'semibold'
  pylab.rcParams[ 'axes.linewidth' ] = 2
  pylab.rcParams[ 'axes.titlesize' ] = 35 - plots / 2
  pylab.rcParams[ 'axes.labelsize' ] = 15 - plots / 2
#  pylab.rcParams[ 'axes.labelweight' ] = 'semibold'
  pylab.rcParams[ 'ytick.major.pad' ] = 9 - plots / 4
  pylab.rcParams[ 'xtick.major.pad' ] = 9 - plots / 4
  pylab.rcParams[ 'xtick.labelsize' ] = 13
  pylab.rcParams[ 'ytick.labelsize' ] = 13
  pylab.rcParams[ 'legend.fontsize' ] = 10 - plots / 1.5
  pylab.rcParams[ 'grid.linewidth' ] = 1

def getCurrent( dataTCT ):
  """It calculates the charge taking into account the gain if the amplifiar from Part$
     www.particulars.si
  """
  voltage = 8
  max_gain = 53
  rel_gain = { 6 : 0.15, 7 : 0.4, 8 : 0.6, 9 : 0.8, 10 : 0.9, 11 : 1, 12 : 1, 13 : 1, 14 : 1, 15 : 1}
  gain = max_gain * rel_gain[ voltage ]
  i = dataTCT.initPoint
  current = []
  corr_curr = []
  trap_time = 30e-8
  while i < dataTCT.endPoint:
    current.append(dataTCT.averageData[i] / ( 50 * gain ))
    i += 1
  i = 0
  while i < len(current):
    corr_curr.append(current[i] * math.exp(i * dataTCT.header[ "xincr" ]/trap_time))
    i += 1
  return current, corr_curr


def convertAndShiftData( dataTCT ):
  """Converts binary to ascii and turns positive signals from p-type
     sensors to negative. The algorithm looks for minimums, not maximums.
  """
  for wave in dataTCT.rawData:
    ywave = dataTCT.data2wave( wave )
    if dataTCT.bulk == "p":
      ywave = list( np.array( ywave ) * -1 )
    dataTCT.pedestalInit, dataTCT.pedestalEnd, pdt = pedestal( ywave )
    dataTCT.ydata = list( np.array( ywave ) - pdt )

def removeElectronicNoise( dataTCT, noiseTCT ):
  for wave in dataTCT.ydata:
    noiseless = np.array( wave ) - np.array( noiseTCT.ydata[ 0 ] )
    dataTCT.noiselessData = list( noiseless )

def averageTheData( dataTCT ):
  """It averages all the waveforms in the file.
  """
  average = np.array( len( dataTCT.noiselessData[ 0 ] ) * [ 0.0 ] )
  for wave in dataTCT.noiselessData:
    average += np.array( wave )
  average /= float( len( dataTCT.noiselessData ) )
  dataTCT.averageData = list( average )

def cutData( dataTCT, cut = "signal" ):
  """ Function that looks for the minimum in the signal and it cuts a 50ns window.
      The window has to begin 1ns before the beginning of the signal and extends
      for 50ns.
      If the argument cut is equal to peak the cut will take only the peak, not 50ns
  """
  window = [ -1e-9, 49e-9 ]
  minimum = dataTCT.averageData.index( min( dataTCT.averageData ) )
  for k in range( len( dataTCT.averageData[ : minimum + 1 ] ) - 1, -1, -1 ):
    if dataTCT.averageData[ k ] > 0.0:
      dataTCT.initSignal = k
      break
  for k in range( minimum, len( dataTCT.averageData )):
    if dataTCT.averageData[ k ] > 0.0:
      dataTCT.endSignal = k
      break
  dataTCT.calculateWindow( window )
  if cut == "peak":
    dataTCT.initPoint = dataTCT.initSignal
    dataTCT.endPoint = dataTCT.endSignal
  elif cut == "signal":
    dataTCT.initPoint = dataTCT.initWindow
    dataTCT.endPoint = dataTCT.endWindow
  elif cut == "whole":
    dataTCT.initPoint = 0
    dataTCT.endPoint = len( dataTCT.average)
  dataTCT.cuttedData = dataTCT.initPoint * [ 0 ] + dataTCT.averageData[ dataTCT.initPoint : dataTCT.endPoint ] + ( len( dataTCT.averageData ) - dataTCT.endPoint ) * [ 0 ]

def pedestal( data ):
  """It calculates the pedestal to eliminate any possible DC in the measure.
  """
  minimum = data.index( min( data ) )
  if minimum / 2 < 3000:
    initPoint = minimum + 2000
    endPoint = minimum + 5000
  else :
    initPoint = 0
    endPoint = minimum / 2
  pedestal = sum( data[ initPoint : endPoint ] ) / float( endPoint - initPoint )
  return initPoint, endPoint, pedestal

def plotResults(filename_tot, xdata_tot, current_tot, init_tot, end_tot,):
  fig = pylab.figure( 1, ( 8, 7 ) )
  n = 0
  voltage = []
  while n <=100:
    voltage.append(n * 10)
    n += 1
  i = 1
  while i < len(current_tot):
    pylab.plot( xdata_tot[i][init_tot[i]:end_tot[i]-800], current_tot[i][0:len(current_tot[i]) - 800], label = str(voltage[i]) + " V")
    i += 10
  pylab.ticklabel_format( axis = 'both', style = 'sci', scilimits = ( 0, 0 ) )
  pylab.legend( loc = 0 )
  pylab.grid( True )
  pylab.xlabel( "Time" )
  pylab.ylabel( "Current" )
  pylab.tight_layout()
  pylab.savefig( "CurrentCombine.png" )
  pylab.close()

def processData( dataTCT, noiseTCT, verbosity, cut = "signal" ):
  """Different steps to finally get the charge from the waveforms
  """
  convertAndShiftData( dataTCT )
  removeElectronicNoise( dataTCT, noiseTCT )
  averageTheData( dataTCT )
  cutData( dataTCT, cut )
  current, corr_curr = getCurrent(dataTCT)
  return current, corr_curr

def natSorting( results ):
  """Natural sorting to save the data in the results file
  """
  indexes = {}
  sorted_data = []
  for line in results:
    indexes[ int( line.split( "\t" )[ 0 ] ) ] = line
  for key in sorted( indexes.keys() )[ : : -1 ]:
    sorted_data.append( indexes[ key ] )
  return sorted_data

def parseador():
  parser = argparse.ArgumentParser( description = "TCT analysis" )
  parser.add_argument( "-f", "--files", type = str, nargs = "+", help = "binary data files" )
  parser.add_argument( "-n", "--noise_file", type = str, help = "electronic noise file" )
  parser.add_argument( "-b", "--bulk", type = str, choices = [ "p", "n" ], default = "n", help = "bulk of the sensor. Choices = n, p. Default = %(default)s", metavar = "" )
  parser.add_argument( "-i", "--integration_window", type = str, choices = [ "signal", "peak", "whole" ], default = "signal", help = "definiton of the integration window, 50ns since the beginning of the peak or only the peak. Choices = signal, peak. Default = %(default)s", metavar = "" )
  parser.add_argument( "-v", "--verbosity", type = int, required = False, default = 1, help = "Verbosity, plots for individual scans are produced only when the verbosity is on. Choices = 0, 1", metavar = "" )
  args = parser.parse_args()
  return args

def getData( dataTCT ):
  """Binary reader and converter to ascii data.
  """
  binreader = BINReader( dataTCT.filename )
  binreader.readData()
  dataTCT.header = binreader.header
  dataTCT.rawData = binreader.data
  binreader.close()

def writeResults( filename, header, results ):
  """Function to write the results in a txt file.
  """
  if os.path.isfile( filename ):
    fd = open( filename, "a" )
  else:
    fd = open( filename, "w" )
    fd.write( header )
  fd.writelines( results )
  fd.close()

def main( files, noiseFile, bulk, integrationWindow, verbosity ):
  results = []
  dataTCT = []
  noiseTCT = TCTData( noiseFile )
  noiseTCT.bulk = bulk
  getData( noiseTCT )
  convertAndShiftData( noiseTCT )
  count = 0
  current_tot = []
  corr_curr_tot = []
  xdata_tot = []
  init_tot = []
  end_tot = []
  filename_tot = []
  for filename in files:
    dataTCT.append( TCTData( filename ) )
    dataTCT[ -1 ].bulk = bulk
    voltage = [ value for value in dataTCT[ -1 ].filename.split( "_" ) if value[ 0 ] == "V" and value[ -1 ] == "V" ][ 0 ].replace( "V", "" )
    getData( dataTCT[ -1 ] )
    current, corr_curr = processData( dataTCT[ -1 ], noiseTCT, verbosity )
    count = count + 1
    current_tot.append(current)
    corr_curr_tot.append(corr_curr)
    xdata_tot.append(dataTCT[-1].xdata)
    init_tot.append(dataTCT[-1].initPoint)
    end_tot.append(dataTCT[-1].endPoint)
    filename_tot.append(dataTCT[-1].filename)
  plotResults(filename_tot, xdata_tot, current_tot, init_tot, end_tot)
  results = natSorting( results )


if __name__ == "__main__":
  args = parseador()
  main( args.files, args.noise_file, args.bulk, args.integration_window, args.verbosity )
