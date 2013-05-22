import os
import json
import logging

from settings import Settings
from core.statspool import StatsPool

logger = logging.getLogger(__name__)

class Project(object):

    def __init__(self):
        self._settings = {}
        self._stats = {}

    def update_settings(self, new_settings):
        self._settings.update(new_settings)

    def get_registered_stats(self):
        return self._stats.keys()

    def get_stats(self, stats_name):
        if stats_name in self._stats:
            return self._stats[stats_name]
        else:
            return None

    def settings(self):
        return self._settings

    def stats(self):
        return self._stats


class __ProjectsSingleton(object):
    _projects = {}

    def load(self):
        search_paths = Settings()['projects']['searchPaths']
        for search_path in search_paths:
            proj_files = [[fname[:-5], os.path.join(search_path,fname)] \
                         for fname in os.listdir(search_path) \
                         if fname.endswith(".conf")]

        self._projects.clear()
        for proj_file in proj_files:
            proj = Project()

            # load the project settings and add the project
            # specific stats path to the common settings
            proj.update_settings(json.load(open(proj_file[1], 'r')))
            Settings()['stats']['searchPaths'].extend(proj.settings()['stats']['searchPaths'])

            # add the project to the list of projects
            if proj_file[0] not in self._projects:
                self._projects[proj_file[0]] = proj
            else:
                logger.error("A project with the name '%s' already exists!"%proj_file[0])


    def create(self):
        for proj_name, proj in self._projects.iteritems():
            # create the stats for this project
            for stat_name in proj.settings()['stats']['register']:
                stat_cls, stat_ins = StatsPool().get(stat_name)
                if stat_ins != None:
                    proj.stats()[stat_name] = stat_ins
                else:
                    logger.error("Couldn't create an instance of stats '%s'!"%stat_name)


    def get(self, proj_name):
        if proj_name in self._projects:
            return self._projects[proj_name]
        else:
            return None

    def list(self):
        return self._projects.keys()



def Projects():
    return __ProjectsSingleton()

