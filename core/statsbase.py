
from pluginmanager.pluginmanager import PluginBase


class StatsBase(PluginBase):

    @staticmethod
    def features():
        return None


    def add(self, data={}, models={}):
        pass


    def get(self, analysis):
        pass