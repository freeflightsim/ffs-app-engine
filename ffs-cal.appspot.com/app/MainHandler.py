# -*- coding: utf-8 -*-

"""
The main handler page 
"""

import os
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template

import gdata.calendar.service

import conf
import app.FFS

class MainHandler(webapp.RequestHandler):


	def get(self, section=None, page=None):
	
		template_vars = {}
		template_vars['conf'] = conf
		template_vars['user'] = None
		
		if section == None:
			section = "index"
		template_vars['section'] = section
		template_vars['page'] = page

		## Application Object
		Appo = app.FFS.FFS()
		template_vars['appo'] = Appo


		if section == 'subscribe' :
				
			if self.request.get("step"):
				step = int(self.request.get("step"))
			else:
				step = 1
			template_vars['step'] = step

			user = users.get_current_user()
			template_vars['user'] = user
			if user:
				template_vars['logout_url'] = users.create_logout_url("/")

 
			"""
			calendar_service = gdata.calendar.service.CalendarService()
			calendar_service.email = 'fg@freeflightsim.org'
			calendar_service.password = 'Airbus747'
			calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
			calendar_service.ProgrammaticLogin()
			"""
			#feed = calendar_service.GetAllCalendarsFeed()
			#print feed.title.text
			#for i, a_calendar in enumerate(feed.entry):
			#	print '\t%s. %s' % (i, a_calendar.title.text,)

			#feed = calendar_service.GetCalendarAclFeed()
			#print feed.title.text
			#for i, a_rule in enumerate(feed.entry):
			#	print '\t%s. %s' % (i, a_rule.title.text,)
			#	print '\t\t Role: %s' % (a_rule.role.value,)
			#	print '\t\t Scope %s - %s' % (a_rule.scope.type, a_rule.scope.value)

			"""
			rule = gdata.calendar.CalendarAclEntry()
			rule.scope = gdata.calendar.Scope(value='ac001@daffodil.uk.com')
			rule.scope.type = 'user'
			roleValue = 'http://schemas.google.com/gCal/2005#%s' % ('freebusy')
			rule.role = gdata.calendar.Role(value=roleValue)
			aclUrl = '/calendar/feeds/fg@freeflightsim.org/acl/full'
			returned_rule = calendar_service.InsertAclEntry(rule, aclUrl)
			"""
			#print "###", returned_rule
			##print "############"

			if page == 'login':
				
				if user:
					##self.response.headers['Content-Type'] = 'text/plain'
					##self.response.out.write('Hello, ' + user.nickname())
					
					template_vars['logout_url'] = users.create_logout_url("/")
				##self.redirect(users.create_login_url(self.request.uri))
				else:
					self.redirect(users.create_login_url("/subscribe/"))

			#main_template = '%s.html' % (section)
			##path = '/%s/' % (section)
		#else:
		main_template = '%s.html' % (section)
		path = '/%s/' % (section)
		template_vars['path'] = path
		#template_vars['title'] = fgApp.title(path)

		

		template_path = os.path.join(os.path.dirname(__file__), '../templates/pages/%s' % main_template)
		self.response.out.write(template.render(template_path, template_vars))

	def post(self, section=None, page=None):
		action = self.request.get('action')
		if action:
			if action == 'add2cal':
				calendar_service = gdata.calendar.service.CalendarService()
				calendar_service.email = 'fg@freeflightsim.org'
				calendar_service.password = 'Airbus747'
				calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
				calendar_service.ProgrammaticLogin()

				rule = gdata.calendar.CalendarAclEntry()
				rule.scope = gdata.calendar.Scope(value='ac001ss4@daffodil.uk.com')
				rule.scope.type = 'user'
				roleValue = 'http://schemas.google.com/gCal/2005#%s' % ('freebusy')
				rule.role = gdata.calendar.Role(value=roleValue)
				aclUrl = '/calendar/feeds/fg@freeflightsim.org/acl/full'
				try:
					returned_rule = calendar_service.InsertAclEntry(rule, aclUrl)
					print returned_rule
				except :
						print "#########"
				