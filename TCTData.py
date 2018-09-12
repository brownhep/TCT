# -*- coding: utf-8 -*-


class TCTData( object ):

  def __init__( self, filename ):
    self.__bulk = ""
    self.__filename = filename
    self.__header = {}
    self.__rawData = []
    self.__xdata = []
    self.__ydata = []
    self.__noiselessData = []
    self.__averageData = []
    self.__cuttedData = []
    self.__pedestalInit = 0
    self.__pedestalEnd = 0
    self.__initSignal = 0
    self.__endSignal = 0
    self.__initWindow = 0
    self.__endWindow = 0
    self.__initPoint = 0
    self.__endPoint = 0

  @property
  def bulk( self ):
    return self.__bulk

  @bulk.setter
  def bulk( self, value ):
    self.__bulk = value

  @property
  def filename( self ):
    return self.__filename

  @property
  def header( self ):
    return self.__header

  @header.setter
  def header( self, value ):
    self.__header = value

  @property
  def rawData( self ):
    return self.__rawData

  @rawData.setter
  def rawData( self, value ):
    self.__rawData = value

  @property
  def xdata( self ):
    return self.__xdata

  @xdata.setter
  def xdata( self, value ):
    self.__xdata = value

  @property
  def ydata( self ):
    return self.__ydata

  @ydata.setter
  def ydata( self, value ):
    self.__ydata.append( value )

  @property
  def noiselessData( self ):
    return self.__noiselessData

  @noiselessData.setter
  def noiselessData( self, value ):
    self.__noiselessData.append( value )

  @property
  def averageData( self ):
    return self.__averageData

  @averageData.setter
  def averageData( self, value ):
    self.__averageData = value

  @property
  def cuttedData( self ):
    return self.__cuttedData

  @cuttedData.setter
  def cuttedData( self, value ):
    self.__cuttedData = value

  @property
  def pedestalInit( self ):
    return self.__pedestalInit

  @pedestalInit.setter
  def pedestalInit( self, value ):
    self.__pedestalInit = value

  @property
  def pedestalEnd( self ):
    return self.__pedestalEnd

  @pedestalEnd.setter
  def pedestalEnd( self, value ):
    self.__pedestalEnd = value

  @property
  def initSignal( self ):
    return self.__initSignal

  @initSignal.setter
  def initSignal( self, value ):
    self.__initSignal = value

  @property
  def endSignal( self ):
    return self.__endSignal

  @endSignal.setter
  def endSignal( self, value ):
    self.__endSignal = value

  @property
  def initWindow( self ):
    return self.__initWindow

  @initWindow.setter
  def initWindow( self, value ):
    self.__initWindow = value

  @property
  def endWindow( self ):
    return self.__endWindow

  @endWindow.setter
  def endWindow( self, value ):
    self.__endWindow = value

  @property
  def initPoint( self ):
    return self.__initPoint

  @initPoint.setter
  def initPoint( self, value ):
    self.__initPoint = value

  @property
  def endPoint( self ):
    return self.__endPoint

  @endPoint.setter
  def endPoint( self, value ):
    self.__endPoint = value

  def data2wave( self, data ):
    """Translates to voltage values the measurements obtained from the oscilloscope TDS3054B.
    """
    ywave = []
    xwave = []
    for i in range( len( data ) ):
      ywave.append( self.header[ "yzero" ] + self.header[ "ymult" ] * ( float( data[ i ] ) - self.header[ "yoff" ] ) )
      xwave.append( self.header[ "xzero" ] + self.header[ "xincr" ] * ( i - self.header[ "pt_off" ] ) )
    if len( self.xdata ) == 0:
      self.xdata = xwave
    return ywave

  def calculateWindow( self, window ):
    self.initWindow = self.initSignal + int( window[ 0 ] / self.header[ 'xincr' ] )
    self.endWindow = self.initSignal + int( window[ 1 ] / self.header[ 'xincr' ] )


if __name__ == "__main__":
  pass
