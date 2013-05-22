
from core.statsbase import StatsBase


class LaunchState(StatsBase):

    @staticmethod
    def features():
        return {'description': "Launch state desc",
                'input': {'launchID' : '',   # expected format of the JSON input data
                          'timestamp' : '',
                          'state' : ''
                         },
                'analyses': []  # string list of supported analyses
               }


    def __init__(self):
        pass


    def add(self, data):
        print data


    def get(self, analysis):
        pass