# -*- coding: utf-8 -*-

"""
The main handler page 
"""

import os
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template


import conf
import app.FFS
import fetch
from app.models import Comment

class MainHandler(webapp.RequestHandler):


	def get(self, section=None, page=None):
	
		template_vars = {}
		template_vars['conf'] = conf
		template_vars['user'] = None
		
		if section == None:
			section = "index"
		template_vars['section'] = section
		template_vars['page'] = page

		#comments(self, section):
		q = db.GqlQuery("SELECT * FROM Comment " +
						"WHERE section = :1  " +
						"ORDER BY dated DESC",
						section)
		results =  q.fetch(50)
		template_vars['comments'] = results

		## Application Object
		Appo = app.FFS.FFS()
		template_vars['appo'] = Appo

		user = users.get_current_user()
		if not user:
			template_vars['user'] = None
			template_vars['login_url'] = users.create_login_url("/subscribe/")		
		else:
			template_vars['user'] = user
			template_vars['logout_url'] = users.create_logout_url("/")
	
		if section == 'subscribe' :
			if not user:
				step = 1
			else:
				cal = fetch.cal_subscribed(user.email())
				if cal == 0:
					step = 2 
				else:
					step = 3
			#if self.request.get("step"):
			#	step = int(self.request.get("step"))
			#else:
			##step = 2
			#template_vars['step'] = step
			#step = 1
			#cal = fetch.cal_subscribed(user.email())	
			#if cal == 0:
			#	step = 2 
			#else:
			#	step = 3

			#else:
			## were logged in
			steps = []
			steps.append({'step': 1, 'label': 'Sign In', 'cls': 'amber' if step == 1 else 'green'})

			if step == 2:
				cls = 'amber'
			elif step > 2:
				cls = 'green'
			else:
				cls = 'red'
			steps.append({'step': 2, 'label': 'Subscribe', 'cls': cls})

			if step == 3:
				cls = 'amber'
			elif step > 3:
				cls = 'green'
			else:
				cls = 'red'
			steps.append({'step': 3, 'label': 'Create Event', 'cls': cls})

			template_vars['steps'] = steps
			#step = 2
			#template_vars['logout_url'] = users.create_logout_url("/subscribe/")


			#if page == 'login':
				
				#if user:
					##self.response.headers['Content-Type'] = 'text/plain'
					##self.response.out.write('Hello, ' + user.nickname())
					
					
				##self.redirect(users.create_login_url(self.request.uri))
				#else:
					#self.redirect(users.create_login_url("/subscribe/"))
			template_vars['step'] = step
			#main_template = '%s.html' % (section)
			##path = '/%s/' % (section)
		#else:

		

		main_template = '%s.html' % (section)
		path = '/%s/' % (section)
		template_vars['path'] = path
		#template_vars['title'] = fgApp.title(path)

		

		template_path = os.path.join(os.path.dirname(__file__), '../templates/pages/%s' % main_template)
		self.response.out.write(template.render(template_path, template_vars))


	###################################################################################################
	def post(self, section=None, page=None):

		action = self.request.get('action')
		#print "actiont", action
		if action:
			## Add User To calendar
			if action == 'add2cal':
				user = users.get_current_user()
				if user:
					app.fetch.cal_add_acl(user.email())
				self.redirect("/subscribe/")
				return

			## Add Comment
			elif action == 'add_comment':
				comment = self.request.get("comment").strip()
				#print "acc comment", comment
				if comment != "":
					
					user = users.get_current_user()
					section = self.request.get("section")
					comm = app.models.Comment(comment=comment, section=section)
					if user:
						comm.author = user
					comm.put()
					#print "acc comment", self.request.get("section"), "/%s/" % section
				self.redirect("/%s/" % section)
				return
		self.redirect("/")
				