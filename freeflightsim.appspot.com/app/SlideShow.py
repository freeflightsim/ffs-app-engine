# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import conf
import app.FFS

class SlideShowHandler(webapp.RequestHandler):


	def get(self, section=None):
	
		template_vars = {}

		## configuration
		template_vars['conf'] = conf

		## Application Calls Object
		Appo = app.FFS.FFS()
		template_vars['appo'] = Appo

		## Set up the enviroment based on section
		if section == None:
			section = "index"

		

		template_path = os.path.join(os.path.dirname(__file__), '../templates/slideshows/%s/index.html' % section)
		self.response.out.write(template.render(template_path, template_vars))

