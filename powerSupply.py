# -*- coding: utf-8 -*-
import time
import math

def setPowerSupply( svoltage, end_voltage, compliance ):
  current_voltage = int( math.ceil( float( svoltage.readVoltage() ) ) )
  svoltage.setCurrentLimit( compliance )
  svoltage.setON()
  if int( end_voltage ) == current_voltage:
    return
  step = ( int( end_voltage ) - current_voltage ) / abs( int( end_voltage ) - current_voltage )
  for i in range( current_voltage, int( end_voltage ) + step, step ):
    svoltage.setVoltage( i )
    time.sleep( 0.1 )

def turnOFFPowerSupply( svoltage ):
  voltage = int( float( svoltage.readVoltage() ) )
  if voltage > 0:
    values = range( int( voltage ), -1, -1 )
  else:
    values = range( int( voltage ), 1, 1 )
  for i in values:
    svoltage.setVoltage( i )
    time.sleep( 0.1 )
  svoltage.setOFF()


if __name__ == "__main__":
  pass
