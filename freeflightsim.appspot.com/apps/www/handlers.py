# -*- coding: utf-8 -*-
"""
	handlers
	~~~~~~~~

	Hello, World!: the simplest tipfy app.

	:copyright: 2009 by tipfy.org.
	:license: BSD, see LICENSE for more details.
"""
from tipfy import RequestHandler, Response
from tipfy.ext.jinja2 import render_response

import site

class Context(object):
	pass

class PageHandler(RequestHandler):
	def get(self, page=None):
		
		c  = Context()
		if page == None:
			c.page = "/"
		else:
			c.page = "/%s" % page
			
		return render_response('circle/index.html', message='Hello, World!', site=site.site, c=c)


class DEADPrettyHelloWorldHandler(RequestHandler):
	def get(self):
		"""Simply returns a rendered template with an enigmatic salutation."""
		return render_response('hello_world.html', message='Hello, World!')
