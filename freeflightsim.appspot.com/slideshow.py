# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import app.SlideShow

application = webapp.WSGIApplication([	('/slidehows/', app.SlideShow.SlidePageHandler),
										('/slidehows/(.*)/', app.SlideShow.SlidePageHandler)
										
									],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()