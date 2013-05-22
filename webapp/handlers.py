import json
import logging
from tornado.web import RequestHandler, HTTPError, asynchronous

from core.projects import Projects
from core.statspool import StatsPool

##### !!!!!!!!!!!!!!!!!!
##### TODO: Validate user input
#####       Where should it go: here or in the classes
#####       Should the classes provide getter and setter and hide the variables
##### !!!!!!!!!!!!!!!!!!


# curl -i -X GET http://localhost:8888/projects
# curl -i -X POST http://localhost:8888/projects -d "{\"key\": \"value\", \"key\": \"value\"}"
# curl -i -X POST http://localhost:8888/projects/scatterCloud/stats/LaunchState -d "{\"aaa\": \"bbbbb\", \"yyyyyy\": \"xxxxx\"}"

class SyncStatsRequestHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')


class CatchAll(SyncStatsRequestHandler):
    pass




class ListAllStats(SyncStatsRequestHandler):
    def get(self):
        self.write({'output': StatsPool().get_available_stats()})


class GetStatsInfo(SyncStatsRequestHandler):
    def get(self, stat_name):
        try:
            features = StatsPool().get_features(stat_name)
            if features is not None:
                self.write({'output': {'features': features}})
            else:
                raise HTTPError(404)
        except:
            raise HTTPError(404)




class ListAllProjects(SyncStatsRequestHandler):
    def get(self):
        self.write({'output': Projects().projects.keys()})


class GetProjectInfo(SyncStatsRequestHandler):
    def get(self, proj_name):
        try:
            self.write({'output': {'settings': Projects().projects[proj_name].settings}})
        except:
            raise HTTPError(404)


class ListProjectStats(SyncStatsRequestHandler):
    def get(self, proj_name):
        self.write({'output': Projects().projects[proj_name].stats.keys()})


class PostStatsData(SyncStatsRequestHandler):
    @asynchronous
    def post(self, proj_name, stat_name):
        try:
            data = json.loads(self.request.body)
            Projects().projects[proj_name].stats[stat_name].add(data)

        except Exception, e:
            raise HTTPError(400)

        self.set_status(202)
        self.finish()





dispatcher = [
    # adapter pool related handlers
    (r'/stats', ListAllStats),
    (r'/stats/([0-9a-zA-Z\-\_]+)', GetStatsInfo),
    # project related handlers
    (r'/projects', ListAllProjects),
    (r'/projects/([0-9a-zA-Z\-\_]+)', GetProjectInfo),
    (r'/projects/([0-9a-zA-Z\-\_]+)/stats', ListProjectStats),
    (r'/projects/([0-9a-zA-Z\-\_]+)/stats/([0-9a-zA-Z\-\_]+)', PostStatsData),
    # catch all
    (r'/.*', CatchAll)
]