# -*- coding: utf-8 -*-

"""
The main handler page 
"""

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import conf
import app.FFS

class MainHandler(webapp.RequestHandler):


	def get(self, section=None, subpage=None):
	
		template_vars = {}

		## configuration
		template_vars['conf'] = conf


		## Application Calls Object
		Appo = app.FFS.FFS()
		template_vars['appo'] = Appo
		#print "##", fgApp.mp_servers_info()

		## Set up the enviroment based on section/subpage eg /download/scenery/
		if section == None:
			section = "index"
		if section and subpage:
			path = '/%s/%s/' % (section, subpage)
			main_template = '%s.%s.html' % (section, subpage)
		elif section:
			path = '/%s/' % (section)
			main_template = '%s.html' % (section)
			
		template_vars['path'] = path
		#template_vars['title'] = fgApp.title(path)

		

		template_path = os.path.join(os.path.dirname(__file__), '../templates/pages/%s' % main_template)
		self.response.out.write(template.render(template_path, template_vars))

