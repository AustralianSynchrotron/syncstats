
import logging
import dateutil.parser
from core import modelutils
from core.statsbase import StatsBase

logger = logging.getLogger(__name__)

class LaunchState(StatsBase):

    @staticmethod
    def features():
        return {'description': "Logs the change of a VM's lauch state",
                'input': {'user': { 'id': 'The user ID [int]',
                                    'name': 'The name of the user [str]',
                                    'email': 'The email of the user [str]'
                                  },
                          'launch': { 'launchID': 'The ID of the launch process [str]',
                                      'state': 'The launch state identifier [str]',
                                      'enter': 'The date/time when the launch state change was entered [datetime iso]',
                                      'leave': 'The date/time when the launch state change was finished [datetime iso]'
                                    }
                         },
                'analyses': []  # string list of supported analyses
               }


    def __init__(self):
        pass


    def set(self, data, project_name):
        from default import models

        usr_data = data['user']
        inp_data = data['launch']

        # get project and user
        prj = modelutils.get_project(project_name)
        usr = modelutils.get_user(usr_data['id'], usr_data['name'], usr_data['email'])

        # Add the launch state to the database
        ls = models.LaunchState(launch_id=inp_data['launchID'],
                                project=prj, user=usr,
                                state=inp_data['state'],
                                enter=dateutil.parser.parse(inp_data['enter']),
                                leave=dateutil.parser.parse(inp_data['leave']))
        ls.save()


    def get(self, analysis):
      #datetime.isoformat
      pass