import json
import logging
from tornado.web import RequestHandler, HTTPError, asynchronous

from core.settings import Settings
from core.projects import Projects
from core.statspool import StatsPool

logger = logging.getLogger(__name__)



class SyncStatsRequestHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        if Settings()['server']['accessControl']['enabled']:
            self.set_header("Access-Control-Allow-Origin", Settings()['server']['accessControl']['allowOrigin'])
            self.set_header("Access-Control-Allow-Credentials", Settings()['server']['accessControl']['allowCredentials'])
            self.set_header("Access-Control-Allow-Methods", Settings()['server']['accessControl']['allowMethods'])
            self.set_header("Access-Control-Allow-Headers", Settings()['server']['accessControl']['allowHeaders'])

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
    def get(self, stats_name):
        try:
            features = StatsPool().get_features(stats_name)
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
            st = Projects().get(proj_name).get_stats(stats_name)
            if st is not None:
                st.set(data, proj_name)
            else:
                logger.error("The project %s doesn't contain the %s stats!"%(proj_name,stats_name))
                raise HTTPError(400)
        except Exception, e:
            logger.error(e)
            raise HTTPError(400)
        self.set_status(202)
        self.finish()

    def get(self, proj_name, stats_name):
        try:
            st = Projects().get(proj_name).get_stats(stats_name)
            if st is not None:
                features = st.features()
                if features is not None:
                    self.write({'output': {'features': features}})
                else:
                    raise HTTPError(404)
            else:
                logger.error("The project %s doesn't contain the %s stats!"%(proj_name,stats_name))
                raise HTTPError(400)
        except Exception, e:
            logger.error(e)
            raise HTTPError(400)


class GetAnalysisData(SyncStatsRequestHandler):
    @asynchronous
    def post(self, proj_name, stats_name, analysis_name):
        try:
            data = json.loads(self.request.body)
            st = Projects().get(proj_name).get_stats(stats_name)
            if st is not None:
                self.write(json.dumps(st.get(analysis_name, data)))
            else:
                logger.error("The project %s doesn't contain the %s stats!"%(proj_name,stats_name))
                raise HTTPError(400)
        except Exception, e:
            logger.error(e)
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
    (r'/projects/([0-9a-zA-Z\-\_]+)/stats/([0-9a-zA-Z\-\_]+)/([0-9a-zA-Z\-\_]+)', GetAnalysisData),
    # catch all
    (r'/.*', CatchAll)
]