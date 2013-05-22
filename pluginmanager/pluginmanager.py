import os
import sys
import imp


class PluginMount(type):
    plugins = {}

    def __init__(cls, name, bases, attrs):
        if cls.features() is not None:
            PluginMount.plugins[cls.__name__] = cls



class PluginBase(object):
    __metaclass__ = PluginMount

    @staticmethod
    def features():
        return None



class PluginManager:

    def load_plugins(self, search_path, skip_filenames=[]):
        PluginMount.plugins = {}
        if not search_path in sys.path:
            sys.path.append(search_path)
        plugin_files = [fname[:-3] for fname in os.listdir(search_path) \
                       if (fname.endswith(".py") and not any(sk in fname for sk in skip_filenames))]
        [__import__(fname) for fname in plugin_files]


    def get_loaded_plugins(self):
        return [name for name in PluginMount.plugins]


    def get_plugin(self, plugin_name):
        if plugin_name in PluginMount.plugins:
            plugin = PluginMount.plugins[plugin_name]
            return plugin, plugin()
        else:
            return None, None


    def get_plugin_features(self, plugin_name):
        if plugin_name in PluginMount.plugins:
            return PluginMount.plugins[plugin_name].features()
        else:
            return None
