import datetime

class DecimalTime(object):
  _secondsPerDay=24*60*60
  _dsecondsPerDay=10*100*100
  _secondsRatio=_secondsPerDay/_dsecondsPerDay

  def __init__(self, dhour, dminute, dsecond):
    self.dhour = dhour
    self.dminute = dminute
    self.dsecond = dsecond

  def __str__(self) -> str:
    str = f"{self.dhour}h{self.dminute}m{self.dsecond:.6f}s"
    return str  
    
  def ratio(self) -> float:
    return (self.dhour*100*100+self.dminute*100+self.dsecond)/DecimalTime._dsecondsPerDay

def from_conventional(time) -> DecimalTime:
  seconds = time.hour*60*60+time.minute*60+time.second+time.microsecond/1e6
  dseconds = seconds/DecimalTime._secondsPerDay*DecimalTime._dsecondsPerDay
  dfractional = dseconds-int(dseconds)
  dseconds = int(dseconds)

  dseconds, dsecond = divmod(dseconds, 100)
  dseconds, dminute = divmod(dseconds, 100)
  dseconds, dhour = divmod(dseconds, 10)
  
  return DecimalTime(dhour, dminute, dsecond+dfractional)
