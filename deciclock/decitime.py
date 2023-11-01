'''
Provides conversion from conventional time 
(24 hours per day, 60 minutes per hour, 60 seconds per minute) to 
decimal time (10 hours per day, 100 minutes per hour, 100 seconds per minute) 
'''
class DecimalTime:
    '''Decimal time (10 hours per day, 100 minutes per hour, 100 seconds per minute)'''
    @staticmethod
    def get_seconds_per_day():
        '''Seconds per day (conventional)'''
        return 24*60*60
    @staticmethod
    def get_dseconds_per_day():
        '''Seconds per day (decimal)'''
        return 10*100*100
    @staticmethod
    def get_conventional_to_decimal_ratio():
        '''Conventional to decimal time ratio'''
        return DecimalTime.get_seconds_per_day()/DecimalTime.get_dseconds_per_day()

    def __init__(self, dhour, dminute, dsecond):
        self.dhour = dhour
        self.dminute = dminute
        self.dsecond = dsecond

    @classmethod
    def from_conventional(cls, time):
        '''Conversion from conventional to decimal time'''
        seconds = time.hour*60*60+time.minute*60+time.second+time.microsecond/1e6
        dseconds = seconds/DecimalTime.get_conventional_to_decimal_ratio()
        dfractional = dseconds-int(dseconds)
        dseconds = int(dseconds)

        dseconds, dsecond = divmod(dseconds, 100)
        dseconds, dminute = divmod(dseconds, 100)
        dseconds, dhour = divmod(dseconds, 10)

        return DecimalTime(dhour, dminute, dsecond+dfractional)

    def ratio(self) -> float:
        '''Return ratio of passed time during a day'''
        dseconds=self.dhour*100*100+self.dminute*100+self.dsecond
        return dseconds/DecimalTime.get_dseconds_per_day()
