
import logging
from core.settings import Settings
from handlers import dispatcher
from tornado import version_info
import tornado.web

def install():
    if version_info[0] >= 3:
        import tornado.log
        tornado.log.enable_pretty_logging()
    else:
        import tornado.options
        tornado.options.enable_pretty_logging()
    
    web_app = tornado.web.Application(dispatcher, debug=Settings()['server']['debug'])
    web_app.listen(Settings()['server']['port'])
    logging.getLogger().setLevel(logging.INFO)
    return web_app
