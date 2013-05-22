
import argparse
from core.statspool import StatsPool
from core.projects import Projects
from core import settings
from core import models
import webapp
from tornado.ioloop import IOLoop

def main():
    # parse the command line arguments
    parser = argparse.ArgumentParser(prog='syncstatsd',
                                     description='SyncStats daemon')
    parser.add_argument('<config_file>', action='store',
                        help='Path to configuration file')
    args = vars(parser.parse_args())
    conf_path = args['<config_file>']

    # load the main configuration file
    settings.read(conf_path)

    # load the project settings and add the paths to the additional stats provided by the projects
    Projects().load()

    # load the stats from the settings file
    StatsPool().load(settings.Settings()['stats']['searchPaths'])

    # initialise the models
    models.init(settings.Settings()['stats']['searchPaths'])

    # create the projects
    Projects().create()

    # Create the database tables if they don't exist yet
    models.create()

    # install the webapp and start the main event loop
    webapp.install()
    IOLoop().instance().start()