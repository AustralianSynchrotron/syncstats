import os
import logging

from settings import Settings
from pluginmanager.pluginmanager import PluginManager

logger = logging.getLogger(__name__)

class __StatsPoolSingleton(object):

    plugin_mgr = PluginManager()

    def __init__(self):
        pass

    def load(self, search_path_list):
        for search_path in search_path_list:
            self.plugin_mgr.load_plugins(search_path, ["models.py"])
            logger.debug("Loading stats from: %s"%search_path)

    def get_available_stats(self):
        return self.plugin_mgr.get_loaded_plugins()

    def get_features(self, stat_name):
        return self.plugin_mgr.get_plugin_features(stat_name)

    def get(self, stat_name):
        return self.plugin_mgr.get_plugin(stat_name)


def StatsPool():
    return __StatsPoolSingleton()