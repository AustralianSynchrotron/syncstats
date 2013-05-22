import os
import json
from settings import Settings
from core.statspool import StatsPool


class Project(object):

    def __init__(self):
        self.settings = {}
        self.stats = {}

    def update_settings(self, new_settings):
        self.settings.update(new_settings)


class __ProjectsSingleton(object):
    projects = {}

    def load(self):
        search_paths = Settings()['projects']['searchPaths']
        for search_path in search_paths:
            proj_files = [[fname[:-5], os.path.join(search_path,fname)] \
                         for fname in os.listdir(search_path) \
                         if fname.endswith(".conf")]

        self.projects.clear()
        for proj_file in proj_files:
            proj = Project()

            # load the project settings and add the project
            # specific stats path to the common settings
            proj.update_settings(json.load(open(proj_file[1], 'r')))
            Settings()['stats']['searchPaths'].extend(proj.settings['stats']['searchPaths'])

            # TODO: check for existing project (logger output)
            self.projects[proj_file[0]] = proj


    def create(self):
        for proj_name, proj in self.projects.iteritems():
            # create the stats for this project
            for stat_name in proj.settings['stats']['served']:
                stat_cls, stat_ins = StatsPool().get(stat_name)
                if stat_ins != None:
                    proj.stats[stat_name] = stat_ins
                else:
                    pass
                    # TODO: error handling




def Projects():
    return __ProjectsSingleton()

