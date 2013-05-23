
from pluginmanager.pluginmanager import PluginBase


class StatsBase(PluginBase):

    @staticmethod
    def features():
        return None


    def set(self, data={}, project_name=""):
        pass


    def get(self, analysis):
        pass