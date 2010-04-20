# -*- coding: utf-8 -*-

import datetime


from google.appengine.ext import db
from google.appengine.api import memcache

from django.utils import simplejson as json
from google.appengine.api import urlfetch

import conf

class FFS:




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



	def __init__(self):
		"""Initialise Navigation and add navigations items"""
		### TODO authenticated sections
		self._mp_servers_info = None
		self.conn = None
		self._nav = []
		self._paths = {}

		self.nav_append( {'path':'/index/', 'label': 'View Calendar'})
		
		self.nav_append( {'path':'/subscribe/', 'label': 'Add An Event'})
		self.nav_append( {'path':'/about/', 'label': 'About'})
		
		"""
		self.nav_append( {'path':'/support/', 'label': 'Support', 
						'subnav': [	
							{'path':'/support/docs/', 'label': 'Documentation'},
							{'path':'/support/faq/', 'label': 'FAQ', 'title': 'Frequently Answered Questions'}
						]
		})

		self.nav_append( {'path':'/download/', 'label': 'Buy', 'title': 'Download Central',
					'subnav': [	
						{'path':'/download/requirements/', 'label': 'Requirements', 'title': 'Hardware Requirements'}, 	
						{'path':'/download/flightgear/', 'label': 'FlightGear', 'title': 'Download FlightGear'}, 	
						#{'path':'/download/aircraft/', 'label': 'Aircraft'},
						{'path':'/download/scenery/', 'label': 'Scenery'},
						{'path':'/download/versions/', 'label': 'Versions', 'title': 'Version Summary'},
					]
		})
		
		self.nav_append( {'path':'/developers/', 'label': 'Developers',
					'subnav': [	
							{'path':'/developers/src/', 'label': 'Source Code'},
							{'path':'/developers/credits/', 'label': 'Credits'}
					]
		})
		self.nav_append( {'path':'/links/', 'label': 'Links',
					'subnav': [	
							{'path':'/links/sites/', 'label': 'Related Sites'},
							{'path':'/links/projects/', 'label': 'Projects'}
					]
		})
		"""

