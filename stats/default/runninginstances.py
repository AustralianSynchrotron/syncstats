
from core.statsbase import StatsBase


class RunningInstances(StatsBase):

    @staticmethod
    def features():
        return {'input' : {},   # expected format of the JSON input data
                'analyses': []  # string list of supported analyses
               }


    def __init__(self):
        pass


    def set(self, data, project_name):
        pass


    def get(self, analysis):
        pass