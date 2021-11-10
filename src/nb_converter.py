import datetime

class Converter:

    def __init__(self):
        pass

    def pytime_to_unixtime(x : datetime.datetime = datetime.datetime.fromisoformat('1950-01-01')) -> int:
        # Setting default time to 1950 since data from that time doesn't exist
        return int(x.timestamp())

    def __del__(self):
        pass
