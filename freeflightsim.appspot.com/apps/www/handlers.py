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

from apps.site import site

class Context(object):
	pass

class PageHandler(RequestHandler):
	def get(self, page=None):
		
		c  = Context()
		if page == None:
			c.page = "/home"
		else:
			c.page = "/%s" % page
			
		return render_response('circle/%s.html' % c.page,  site=site, c=c)


