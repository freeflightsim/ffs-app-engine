# -*- coding: utf-8 -*-

import time
import datetime
from google.appengine.ext import webapp
from django.utils import simplejson as json
from google.appengine.ext import db

import conf
from app.models import FPp, Cookie, Comment

class RpcHandler(webapp.RequestHandler):


	def get_schedule(self):
		lst = []
		entries = db.GqlQuery("select * from FPp order by dep_date asc")
		for e in entries:
			lst.append(self.fpp_dic(e))
		return lst

	def fpp_dic(self, e):
		dic = {'callsign': e.callsign, 'fppID': str(e.key()),
			'comment': e.comment,
			'dep': e.dep, 'dep_date': e.dep_date.strftime(conf.MYSQL_DATETIME), 'dep_atc': e.dep_atc,
			'arr': e.arr, 'arr_date': e.arr_date.strftime(conf.MYSQL_DATETIME), 'arr_atc': e.arr_atc
			}
		return dic

	def get(self, action):
		self.post(action)

	def post(self, action):
	
		reply = {'success': True }

		########################################################
		### Index
		if action == 'index':
			reply['schedule'] = self.get_schedule()


		########################################################
		### TimeLIne
		elif action == 'timeline':
			cols = {}
			reverse = {}
			#cols.append({'label': 'Pilot'})
			#cols.append({'label': 'Airport'})
			tod = datetime.datetime.now()
			SECS_IN_HOUR = 60 * 60 * 50
			y = tod.year
			m = tod.month
			d =  tod.day
			h =  tod.hour
			for c in range(0, 24):
				nt = datetime.datetime(y, m, d, h, 0, 0)
				#print c, tod, nt
				h = h + 1
				if h == 24:
					h = 0
					d = d + 1
				#for c in range(-1, 25):
				col_ki = 'col_%s' % c 
				cols[col_ki] =  nt.strftime("%H");
				reverse[h] = col_ki
			reply['cols'] = cols

			#entries = db.GqlQuery("select * from FPp order by dep_date asc")
			rows = []
			rowsX = {}
			q = FPp.all()
			#q.filter('dep_date >=', tod)
			q.order('dep_date');
			scheds = q.fetch(100)
			for e in scheds:
				if e.dep:
					col_ki = 'col_%s' % int(e.dep_date.strftime("%H"))
					dic = { 'time': e.dep_date.strftime("%H:%M"), 'col_ki': col_ki, 'fppID': str(e.key()),
							'mode': 'dep', 'airport':e.dep, 'callsign': e.callsign }
					rows.append(dic)
				if e.arr:
					col_ki = 'col_%s' % int(e.arr_date.strftime("%H")) 
					dic = {	'time': e.arr_date.strftime("%H:%M"), 'col_ki': col_ki,'fppID': str(e.key()),
							'mode': 'arr', 'airport':e.arr, 'callsign': e.callsign}
					#rowsX[col_ki] = dic
					rows.append(dic)
			reply['rows'] = rows

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
					dic = {	'callsign': '', 
							'email': '',
							'dep': '',
							'dep_date': d.strftime(conf.MYSQL_DATETIME),
							'dep_atc': '',
							'arr': '',
							'arr_date': '',
							'arr_atc': '',
							'comment': '',
							'fppID': '0'
					}

				else:
					f = db.get( db.Key(fppID) )
					dic = {	'callsign': f.callsign, 
							'email': 'email',
							'dep': f.dep,
							'dep_date': f.dep_date.strftime(conf.MYSQL_DATETIME),
							'dep_atc': f.dep_atc,
							'arr': f.arr,
							'arr_date': f.arr_date.strftime(conf.MYSQL_DATETIME),
							'arr_atc': f.arr_atc,
							'comment': f.comment,
							'fppID': str(f.key()),
					}
				reply['fpp'] = dic

		########################################################
		### Edit
		elif action == 'edit':
			fppID = self.request.get("fppID")
			if not fppID:
				reply['error'] = 'No fppID'
			else:
				callsign = self.request.get("callsign")
				if fppID == '0':
					fp = FPp(callsign = callsign)
				else:
					fp = db.get( db.Key(fppID) )
					fp.cookie = self.request.cookies['sessID'] 
					fp.callsign = callsign
				fp.dep = self.request.get("dep")
				fp.dep_date = self.get_date(self.request.get("dep_date"), self.request.get("dep_time"))
				
				fp.dep_atc = self.request.get("dep_atc")

				fp.arr = self.request.get("arr")
				fp.arr_date = self.get_date(self.request.get("arr_date"), self.request.get("arr_time"))
				fp.arr_atc = self.request.get("arr_atc")

				fp.comment = self.request.get("comment")
				fp.email = self.request.get("email")
				fp.put()
				reply['schedule'] = self.get_schedule()

		self.response.headers.add_header('Content-Type','text/plain')
		self.response.out.write(json.dumps(reply))

	def get_date(self, dt, tt):
		#self.response.out.write(json.dumps({dt: tt}))
		return datetime.datetime.strptime( '%s %s:00' % (dt, tt) , conf.MYSQL_DATETIME)