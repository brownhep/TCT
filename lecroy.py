# -*- coding: utf-8 -*-


from OOHw.interface.InterfaceFactory import InterfaceFactory
from OOHw.files.BINWriter import BINWriter
import time


factory = InterfaceFactory( "lecroy.ini" )
lecroy = factory.getDevice( "scope" )
print lecroy.getId()
#lecroy.channel = "C4"
#lecroy.function = "F2"
#lecroy.write( """%s:DEF EQN,"G(%s)",AVERAGETYPE,SUMMED,SWEEPS,512""" % ( lecroy.function, lecroy.channel ) )
#lecroy.trace( lecroy.channel, "ON" )
#lecroy.trace( lecroy.function, "ON" )
#lecroy.clearSweeps()
#t1 = time.time()
#while lecroy.obtainPreamble( lecroy.function )[ "SWEEPS_PER_ACQ" ] != "512":
#  print lecroy.obtainPreamble( lecroy.function )[ "SWEEPS_PER_ACQ" ]
#  time.sleep( .5 )
#print lecroy.preamble
#print time.time() - t1
#lecroy.opc()
#waveform, points, bytesPoint = lecroy.readWaveformBIN( lecroy.function )
#binwriter = BINWriter( "bbb2.bin" )
#binwriter.header = lecroy.preamble
#binwriter.addData( waveform )
#binwriter.bytesPerPoint( bytesPoint )
#binwriter.pointsPerMeasurement( points )
#binwriter.writeData()
#binwriter.close()
