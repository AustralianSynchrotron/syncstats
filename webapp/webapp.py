
import logging
from core.settings import Settings
from handlers import dispatcher
from tornado import version_info
import tornado.web

def install():
    web_app = tornado.web.Application(dispatcher, debug=Settings()['server']['debug'])
    web_app.listen(Settings()['server']['port'])
    return web_app
