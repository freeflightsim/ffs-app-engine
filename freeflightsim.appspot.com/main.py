# -*- coding: utf-8 -*-

"""
This is the main handler and is responsible of the public html area.
"""


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import app.Handler

application = webapp.WSGIApplication([	('/(.*)/(.*)/', app.Handler.PageHandler),
										('/(.*)/', app.Handler.PageHandler),
										('/', app.Handler.PageHandler),
										
									],
									debug=conf.DEBUG)


if __name__ == "__main__":
	run_wsgi_app(application)