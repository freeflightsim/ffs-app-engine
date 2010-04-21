# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import conf
import app.MainHandler

if os.environ.get('SERVER_SOFTWARE','').startswith('Devel'):
    DEBUG = True
else:
    DEBUG = False

application = webapp.WSGIApplication([	('/rpc/(.*)/', app.MainHandler.RpcHandler),
										('/(.*)/(.*)/', app.MainHandler.MainHandler),
										('/(.*)/', app.MainHandler.MainHandler),
										('/', app.MainHandler.MainHandler),
										
									],
									debug=DEBUG)


if __name__ == "__main__":
	run_wsgi_app(application)