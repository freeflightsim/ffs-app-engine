# -*- coding: utf-8 -*-


import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import mail

from django.utils import simplejson as json
from google.appengine.api import urlfetch
import urllib
import Cookie

import conf
import app.FFS
##import fetch
from app.models import Comment

class AuthHandler(webapp.RequestHandler):

	###################################################################################################
	## Get Actions
	###################################################################################################
	def get(self):
		self.post()
		return
		template_vars = {}
		template_vars['conf'] = conf
		template_vars['user'] = None
		
		section = "foo"

		main_template = '%s.html' % (section)
		path = '/%s/' % (section)
		template_vars['path'] = path
	

		template_path = os.path.join(os.path.dirname(__file__), '../templates/pages/%s' % main_template)
		self.response.out.write(template.render(template_path, template_vars))



	###################################################################################################
	## Post Actions
	###################################################################################################
	def post(self, section=None, page=None):

		token = self.request.get('token')
		url = 'https://rpxnow.com/api/v2/auth_info'
		args = {
			'format': 'json',
			'apiKey': conf.RPX_API_KEY,
			'token': token
		}

		r = urlfetch.fetch(	url=url,
							payload=urllib.urlencode(args),
							method=urlfetch.POST,
							headers={'Content-Type':'application/x-www-form-urlencoded'}
		)
		#print url
		data = json.loads(r.content)
		#print data, r.content
		if data['stat'] == 'ok':   
			unique_identifier = data['profile']['identifier']
			nickname = data['profile']['preferredUsername']
			email = data['profile']['email']
	
			

			# log the user in using the unique_identifier
			# this should your cookies or session you already have implemented
			#self.log_user_in(unique_identifier)   
			#self.redirect('/?' + urllib.urlencode(data ))
		#else:
			#self.redirect('/error') 
		s	= "section=%s\n" % section
		s += "page=%s\n" % page
		s += r.content

		self.response.out.write(s)