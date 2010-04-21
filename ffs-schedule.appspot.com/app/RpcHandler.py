# -*- coding: utf-8 -*-

import time
import datetime
from google.appengine.ext import webapp
from django.utils import simplejson as json
from google.appengine.ext import db

import conf
from app.models import FPp, Cookie, Comment

class RpcHandler(webapp.RequestHandler):


	def get(self, action):
		self.post(action)

	def post(self, action):
	
		reply = {'success': True }

		########################################################
		### Index
		if action == 'index':
			lst = []
			entries = db.GqlQuery("select * from FPp order by dep_date asc")
			for e in entries:
				lst.append({'callsign': e.callsign, 'fppID': str(e.key()),
							'comment': e.comment,
							'dep': e.dep, 'dep_date': e.dep_date.strftime(conf.MYSQL_DATETIME), 'dep_atc': e.dep_atc,
							'arr': e.arr, 'arr_date': e.arr_date.strftime(conf.MYSQL_DATETIME), 'arr_atc': e.arr_atc
							})
			reply['schedule'] = lst

		########################################################
		### Fetch 
		elif action == 'fetch':
			fppID = self.request.get("fppID")
			if not fppID:
				reply['error'] = 'No fppID'

			else:
				if fppID == '0':
					t = time.time()
					d = datetime.datetime.fromtimestamp(t - t % (60 *15) )
					dic = {	'callsign': 'callsign', 
							'email': 'email',
							'dep': 'EGLL',
							'dep_date': d.strftime(conf.MYSQL_DATETIME),
							'dep_atc': 'atdc',
							'arr': 'EGFF',
							'arr_date': d.strftime(conf.MYSQL_DATETIME),
							'arr_atc': 'aaaatdc',
							'comment': 'comment',
							'fppID': '0',
							't': '%s' % t
					}
					reply['fpp'] = dic
				else:
					reply['fpp'] = {'YES': 'NO'}

		########################################################
		### Edit
		elif action == 'edit':
			
			

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

		self.response.headers.add_header('Content-Type','text/plain')
		self.response.out.write(json.dumps(reply))

	def get_date(self, dt, tt):
		#self.response.out.write(json.dumps({dt: tt}))
		return datetime.datetime.strptime( '%s %s:00' % (dt, tt) , conf.MYSQL_DATETIME)