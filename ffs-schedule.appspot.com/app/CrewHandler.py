# -*- coding: utf-8 -*-

import os
import time
import datetime

from google.appengine.ext import webapp
from django.utils import simplejson as json
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import urlfetch
import urllib

import conf
from app.models import Crew
import app.FFS





class CrewHandler(webapp.RequestHandler):

	def do_cookie_check(self):
		if 'sessID' in self.request.cookies:
			return  self.request.cookies['sessID'] 
		else:
			return None


	def get(self, section):

		sessID = self.do_cookie_check()
	
		template_vars = {}
		template_vars['conf'] = conf
		template_vars['user'] = None
		template_vars['sessID'] = sessID
		template_vars['section'] = section

		if section == 'profile':
			if not sessID:
				self.redirect("/signin/")
				return

	
			## Setup Section and Page
			#if section == None:
			#	section = "index"
			
			#template_vars['page'] = page
			
			
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


			#crew = db.get( db.Key(sessID) )
			#template_vars['crew'] = crew

			template_path = os.path.join(os.path.dirname(__file__), '../templates/pages/%s.html' % section)
			self.response.out.write(template.render(template_path, template_vars))





	def post(self, action):
	

		if action == 'auth':

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
			data = json.loads(r.content)

			if data['stat'] == 'ok':   
				welcome = 0
				unique_identifier = data['profile']['identifier']
				
				q = db.GqlQuery("select * from Crew where ident= :1", unique_identifier)
				crew = q.get()
				if not crew:
					crew = Crew(ident=unique_identifier)
					crew.name = nickname = data['profile']['preferredUsername']
					if data['profile'].has_key('email'):
						crew.email = data['profile']['email']
					crew.put()
					welcome = 1

				sessID = str(crew.key())
				cook_str = 'sessID=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT; Path=/;'	% sessID
				self.response.headers.add_header(	'Set-Cookie', 
													cook_str
				)

				#tvars = {'welcome': welcome, 'sessID': sessID, 'cook_str':cook_str}				
				self.redirect("/crew/profile/?welcome=%s" % welcome)
				return	
			else:
				pass
				
			
		########################################################
		### Send
		self.response.headers.add_header('Content-Type','text/plain')
		self.response.out.write(json.dumps(data))
