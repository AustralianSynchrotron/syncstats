
from pluginmanager.pluginmanager import PluginBase


class StatsBase(PluginBase):

    @staticmethod
    def features():
        return None


    def set(self, data={}, project_name=""):
        pass


    def get(self, analysis_name, data):
      return getattr(self, analysis_name)(analysis_name, data)