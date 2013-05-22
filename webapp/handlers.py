import json
import logging
from tornado.web import RequestHandler, HTTPError, asynchronous

from core.projects import Projects
from core.statspool import StatsPool

logger = logging.getLogger(__name__)

##### !!!!!!!!!!!!!!!!!!
##### TODO: Validate user input
#####       Where should it go: here or in the classes
#####       Should the classes provide getter and setter and hide the variables
##### !!!!!!!!!!!!!!!!!!


# curl -i -X GET http://localhost:8888/projects
# curl -i -X GET http://localhost:8888/projects/scatterCloud
# curl -i -X POST http://localhost:8888/projects/scatterCloud/stats/LaunchState -d "{\"aaa\": \"bbbbb\", \"yyyyyy\": \"xxxxx\"}"

class SyncStatsRequestHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')


class CatchAll(SyncStatsRequestHandler):
    def get(self):
        logger.warning("No handler available for: %s %s"%(self.request.method, self.request.uri))

    def post(self):
        logger.warning("No handler available for: %s %s"%(self.request.method, self.request.uri))




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
        self.write({'output': Projects().list()})


class GetProjectInfo(SyncStatsRequestHandler):
    def get(self, proj_name):
        try:
            self.write({'output': {'settings': Projects().get(proj_name).settings()}})
        except:
            raise HTTPError(404)


class ListProjectStats(SyncStatsRequestHandler):
    def get(self, proj_name):
        self.write({'output': Projects().get(proj_name).get_registered_stats()})


class PostStatsData(SyncStatsRequestHandler):
    @asynchronous
    def post(self, proj_name, stats_name):
        try:
            data = json.loads(self.request.body)
            print proj_name, stats_name
            st = Projects().get(proj_name).get_stats(stats_name)
            if st is not None:
                st.add(data)
            else:
                logger.error("The project %s doesn't contain the %s stats!"%(proj_name,stats_name))
                raise HTTPError(400)
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