# -*- coding: utf-8 -*-

"""
This is the script that runs for most pages,
it starts a wsgi application
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

## Load Configuation
import conf

## Load main handler class
import app.MainHandler


application = webapp.WSGIApplication([	('/(.*)/(.*)/', app.MainHandler.MainHandler),
										('/(.*)/', app.MainHandler.MainHandler),
										('/', app.MainHandler.MainHandler),
										
									],
									debug=conf.DEBUG)


if __name__ == "__main__":
	run_wsgi_app(application)