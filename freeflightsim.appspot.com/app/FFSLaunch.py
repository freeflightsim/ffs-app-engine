# -*- coding: utf-8 -*-

import datetime
import random

from google.appengine.ext import db
from google.appengine.api import memcache

from django.utils import simplejson as json
from google.appengine.api import urlfetch


import conf
#import app.fetch

##############################################################
## App Calls Class
##############################################################
class FFSLaunch:


	## Gallery
	def gallery(self):
		return app.fetch.gallery()

	def random_image(self):
		return app.fetch.gallery_random()

	def nav(self):
		"""Return navigation - used in tempalte """
		return self._nav

	def title(self, path):
		"""Return the title or label from path based lookup"""
		if path in self._paths:
			if 'title' in self._paths[path]:
				return  self._paths[path]['title']
			else:
				return  self._paths[path]['label']
		return "#### NO TITLE ###"


	def nav_append(self, dic):
		"""Append items to navigations"""
		self._nav.append(dic)
		self._paths[dic['path']] = dic
		if 'subnav' in dic:
			for subpage in dic['subnav']:
				self._paths[subpage['path']] = subpage


	def mp_servers_info(self):
		return app.fetch.mp_servers_info()


	def __init__(self):
		"""Initialise Navigation and add navigations items"""
		### TODO authenticated sections
		self._mp_servers_info = None

		self._nav = []
		self._paths = {}

		self.nav_append( {'path':'/index/', 'label': 'Index', 'title': 'Welcome',
						'subnav': [	
							{'path':'/index/announce/', 'label': 'Announcements', 'title': 'News and announcments'},
							{'path':'/index/calendar/', 'label': 'Calendar', 'title': 'Calendar'},
						]
		})

		self.nav_append( {'path':'/reception/', 'label': 'Reception', 'title': 'About Free Flight Sim.org',
						'subnav': [	
							{'path':'/about/features/', 'label': 'Features' },
							{'path':'/about/license/', 'label': 'License'}
						]
		})

		self.nav_append( {'path':'/atc/', 'label': 'ATC', 
						'subnav': [	
							{'path':'/media/videos/', 'label': 'Videos', 'title': 'Videos'},
							{'path':'/media/gallery/', 'label': 'Image Gallery'}
						]
		})

		self.nav_append( {'path':'/fgcom/', 'label': 'FgCom', 
						'subnav': [	
							{'path':'/support/docs/', 'label': 'Documentation'},
							{'path':'/support/faq/', 'label': 'FAQ', 'title': 'Frequently Answered Questions'}
						]
		})

		self.nav_append( {'path':'/school/', 'label': 'Flight School', 'title': 'Download Central',
					'subnav': [	
						{'path':'/download/requirements/', 'label': 'Requirements', 'title': 'Hardware Requirements'}, 	
						{'path':'/download/flightgear/', 'label': 'FlightGear', 'title': 'Download FlightGear'}, 	
						#{'path':'/download/aircraft/', 'label': 'Aircraft'},
						{'path':'/download/scenery/', 'label': 'Scenery'},
						{'path':'/download/versions/', 'label': 'Versions', 'title': 'Version Summary'},
					]
		})
		
		self.nav_append( {'path':'/clubs/', 'label': 'Flight Clubs',
					'subnav': [	
							{'path':'/developers/src/', 'label': 'Source Code'},
							{'path':'/developers/credits/', 'label': 'Credits'}
					]
		})
		self.nav_append( {'path':'/airlines/', 'label': 'Virtual Airlines',
					'subnav': [	
							{'path':'/links/sites/', 'label': 'Related Sites'},
							{'path':'/links/projects/', 'label': 'Projects'}
					]
		})


