# -*- coding: utf-8 -*-


import os
import uuid
import datetime
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.ext.webapp import template
from django.utils import simplejson as json

import conf
import app.FFS
import fetch
from app.models import FPp, Cookie, Comment

class MainHandler(webapp.RequestHandler):

	def do_cookie_check(self):
		if 'sessID' in self.request.cookies:
			return  self.request.cookies['sessID'] 
		else:
			sessID = str(uuid.uuid1())
			cook = Cookie(sessID=sessID)
			cook.put()
			self.response.headers.add_header(	'Set-Cookie', 
												'sessID=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT'	% sessID
			)
			return sessID

	###################################################################################################
	## Get Actions
	###################################################################################################
	def get(self, section=None, page=None):
	
		cook = self.do_cookie_check()

		template_vars = {}
		template_vars['now'] = datetime.datetime.now()
		template_vars['conf'] = conf
		template_vars['user'] = None
		template_vars['cook'] = cook
		
		## Setup Section and Page
		if section == None:
			section = "index"
		template_vars['section'] = section
		template_vars['page'] = page
		

		## Get Comments
		q = db.GqlQuery("SELECT * FROM Comment " +
						"WHERE section = :1  " +
						"ORDER BY dated DESC",
						section)
		results =  q.fetch(50)
		template_vars['comments'] = results

		## Application Object
		Appo = app.FFS.FFS()
		template_vars['appo'] = Appo
		template_vars['page_title'] = Appo.title("/%s/" % section)


		## Setup User + Aauth
		user = users.get_current_user()
		if not user:
			template_vars['user'] = None
			template_vars['login_url'] = users.create_login_url("/set_session/")		
		else:
			template_vars['user'] = user
			template_vars['logout_url'] = users.create_logout_url("/subscribe/")

		## Subscribe Section
		if user and section == 'set_session':
			mail.send_mail(	sender = conf.EMAIL,
							to = "Dev <dev@freeflightsim.org>",
							subject = "Login: %s" % user.email(),
							body = "OK"
			)
			self.redirect("/subscribe/")
			return
	
		## Subscribe Section
		if section == 'subscribe' :
			if not user:
				step = 1
			else:
				cal = fetch.cal_subscribed(user.email())
				if cal == 0:
					step = 2 
				else:
					step = 3
	
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
			template_vars['step'] = step
	

		main_template = '%s.html' % (section)
		path = '/%s/' % (section)
		template_vars['path'] = path
	

		template_path = os.path.join(os.path.dirname(__file__), '../templates/pages/%s' % main_template)
		self.response.out.write(template.render(template_path, template_vars))



	###################################################################################################
	## Post Actions
	###################################################################################################
	def post(self, section=None, page=None):

		action = self.request.get('action')
	
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
				if comment != "":
					
					user = users.get_current_user()
					section = self.request.get("section")
					comm = app.models.Comment(comment=comment, section=section)
					if user:
						comm.author = user
					comm.put()
					mail.send_mail(	sender = conf.EMAIL,
									to = "Dev <dev@freeflightsim.org>",
									subject = "Comment on: %s" % section,
									body = comment
					)
					self.redirect("/%s/" % section)
					return
		self.redirect("/")
				
















class RpcHandler(webapp.RequestHandler):


	def get(self, action):
		self.post(action)

	def post(self, action):
	
		#if self.request.get("fppID"):
			#// update
		#	pass
		#else:

		fp = FPp(callsign =self.request.get("callsign"))
		fp.cookie = self.request.cookies['sessID'] 

		fp.dep = self.request.get("dep")
		fp.dep_date = self.get_date(self.request.get("dep_date"), self.request.get("dep_time"))
		
		fp.dep_atc = self.request.get("dep_atc")

		fp.arr = self.request.get("arr")
		fp.arr_date = self.get_date(self.request.get("arr_date"), self.request.get("arr_time"))
		fp.arr_atc = self.request.get("arr_atc")

		fp.comment = self.request.get("comment")
		fp.email = self.request.get("email")
		fp.put()
		self.response.headers.add_header(	'Content-Type', 
											'text/plain'
		)
		data = {'success': True }
		self.response.out.write(json.dumps(data))

	def get_date(self, dt, tt):
		#self.response.out.write(json.dumps({dt: tt}))
		return datetime.datetime.strptime( '%s %s:00' % (dt, tt) , '%Y-%m-%d %H:%M:%S')