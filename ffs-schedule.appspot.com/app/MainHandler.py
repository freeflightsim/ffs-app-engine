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
#import fetch
from app.models import FPp,  Comment



class MainHandler(webapp.RequestHandler):


	def do_cookie_check(self):
		if 'sessID' in self.request.cookies:
			return  self.request.cookies['sessID'] 
		else:
			return None

	###################################################################################################
	## Get Actions
	###################################################################################################
	def get(self, section=None, page=None):
	
		sessID = self.do_cookie_check()



		template_vars = {}
		template_vars['conf'] = conf
		template_vars['user'] = None
		template_vars['sessID'] = sessID
		if 'sessIdent' in self.request.cookies:
			sessIdent =  self.request.cookies['sessIdent'] 
		else:
			sessIdent = None
		template_vars['profile_label'] = "%s Profile" % sessIdent if sessIdent else "My Profile"

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
		#user = users.get_current_user()
		#if not user:
		#	template_vars['user'] = None
		#	template_vars['login_url'] = users.create_login_url("/set_session/")		
		#else:
		#	template_vars['user'] = user
		#	template_vars['logout_url'] = users.create_logout_url("/subscribe/")

	
		## Subscribe Section
		if section == 'signin' :
			if sessID:
				self.redirect("/crew/profile/")
				return 
			template_vars['page_title'] = 'Sign In with OpenId'

		if section == 'do_logout':
				cook_str = 'sessID=%s; expires=Fri, 31-Dec-1980 23:59:59 GMT; Path=/;'	% ''
				self.response.headers.add_header(	'Set-Cookie', 
													cook_str
				)
				self.redirect("/")
				return


		if section == 'profile':
			if not sessID:
				self.redirect("/signin/")
				return
			template_vars['page_title'] = 'My Profile'
	

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

			## Add Comment
			if action == 'add_comment':
				comment = self.request.get("comment")
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
				













