import os
import sys
import json

from string import Template

class __SettingsSingleton(object):
    d = {}


def Settings():
    return __SettingsSingleton().d


def read(conf_path):
    # get absolute path of the settings file and the daemon
    # for replacing the templates in the settings file
    repl_paths = {"settings_path": os.path.abspath(os.path.dirname(conf_path)),
                  "daemon_path": sys.path[0]
                 }

    # read the settings file, replace the path templates and
    # store the result into the dictionary
    Settings().clear()
    settings_file = open(conf_path, 'r')
    set_temp = Template(settings_file.read())
    Settings().update(json.loads(set_temp.safe_substitute(repl_paths)))
    settings_file.close()
