'''
Provides conversion from conventional time 
(24 hours per day, 60 minutes per hour, 60 seconds per minute) to 
decimal time (10 hours per day, 100 minutes per hour, 100 seconds per minute) 
'''
class DecimalTime:
    '''Decimal time (10 hours per day, 100 minutes per hour, 100 seconds per minute)'''
    _secondsPerDay=24*60*60
    _dsecondsPerDay=10*100*100
    _secondsRatio=_secondsPerDay/_dsecondsPerDay

    def __init__(self, dhour, dminute, dsecond):
        self.dhour = dhour
        self.dminute = dminute
        self.dsecond = dsecond

    def ratio(self) -> float:
        '''Return ratio of passed time during a day'''
        return (self.dhour*100*100+self.dminute*100+self.dsecond)/DecimalTime._dsecondsPerDay

def from_conventional(time) -> DecimalTime:
    '''Conversion from conventional to decimal time'''
    seconds = time.hour*60*60+time.minute*60+time.second+time.microsecond/1e6
    dseconds = seconds/DecimalTime._secondsRatio
    dfractional = dseconds-int(dseconds)
    dseconds = int(dseconds)

    dseconds, dsecond = divmod(dseconds, 100)
    dseconds, dminute = divmod(dseconds, 100)
    dseconds, dhour = divmod(dseconds, 10)

    return DecimalTime(dhour, dminute, dsecond+dfractional)
