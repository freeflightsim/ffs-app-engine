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
			lst.append({	'callsign': e.callsign, 'fppID': str(e.key()),
						'comment': e.comment,
						'dep': e.dep, 'dep_date': e.dep_date.strftime(conf.MYSQL_DATETIME), 'dep_atc': e.dep_atc,
						'arr': e.arr, 'arr_date': e.arr_date.strftime(conf.MYSQL_DATETIME), 'arr_atc': e.arr_atc
			})
		return lst

	def get_timeline(self):
		reply = {}
		SECS_IN_HOUR = 60 * 60 
		
		################### current, start and end dates
		n = datetime.datetime.utcnow()
		curr_ts = time.mktime((n.year, n.month, n.day, n.hour, 0, 0, 0, 0, 0))
		curr_dt = datetime.datetime.fromtimestamp(curr_ts)
		reply['current_date'] = curr_dt.strftime(conf.MYSQL_DATETIME)

		start_ts = curr_ts - SECS_IN_HOUR
		start_dt = datetime.datetime.fromtimestamp(start_ts)
		reply['start_date'] = start_dt.strftime(conf.MYSQL_DATETIME)

		end_ts = curr_ts + (SECS_IN_HOUR * 30)
		end_dt = datetime.datetime.fromtimestamp(end_ts)
		reply['end_date'] = end_dt.strftime(conf.MYSQL_DATETIME)

		########################## Cols
		col_no = 0
		cols = {}
		reverse = {}
		rev_ki = "%d_%H"
		for c in range(-1, 33):
			col_time = datetime.datetime.fromtimestamp(curr_ts + (SECS_IN_HOUR * c))
			ki = "col_%s" % col_no
			cols[ki] =  str(int(col_time.strftime("%H")))
			reverse[col_time.strftime(rev_ki)] = ki
			col_no += 1
		reply['cols'] = cols

		####################### Rows
		rows = []
		rowsX = {}
		q = FPp.all()
		#q.filter('dep_date >=', tod)
		q.order('dep_date');
		scheds = q.fetch(100)
		rows = []
		for e in scheds:
			cols = []

			## Departure
			if reverse.has_key( e.dep_date.strftime(rev_ki)):
				cols.append({	'col_ki': reverse[e.dep_date.strftime(rev_ki)],
								'time': e.dep_date.strftime("%M"), 
								'mode': 'dep'
				})

			## Arrival
			if reverse.has_key( e.arr_date.strftime(rev_ki) ):
				cols.append({	'col_ki': reverse[e.arr_date.strftime(rev_ki)],
								'time': e.arr_date.strftime("%M"), 
								'mode': 'dep'
				})

			## loop the middle
			loop_ts = time.mktime((e.dep_date.year, e.dep_date.month, e.dep_date.day, e.dep_date.hour, 0, 0, 0, 0, 0)) + SECS_IN_HOUR
			last_ts = time.mktime((e.arr_date.year, e.arr_date.month, e.arr_date.day, e.arr_date.hour, 0, 0, 0, 0, 0)) 
			hr =  0
			while loop_ts < last_ts:
				loop_time = datetime.datetime.fromtimestamp(loop_ts )
				if reverse.has_key(loop_time.strftime(rev_ki)):
					cols.append({'col_ki': reverse[loop_time.strftime(rev_ki)],
							'time': loop_time.strftime("%M"), 'mode': 'mid'
					})
				loop_ts = loop_ts + SECS_IN_HOUR 
			
			data = {'callsign': e.callsign, 'cols': cols, 'dep': e.dep, 'arr': e.arr, 'fppID': str(e.key())}
			rows.append(data)
		reply['rows'] = rows
		return reply


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
			reply['timeline'] = self.get_timeline()



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