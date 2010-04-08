# -*- coding: utf-8 -*-
from google.appengine.ext import db

"""
The Data Definition
"""

class FOOAero(db.Model):
	aero = db.StringProperty(indexed=True)
	directory =  db.StringProperty(indexed=True)
	description = db.StringProperty(indexed=True)
	splash = db.StringProperty()
	fdm = db.StringProperty(indexed=True)
	status = db.StringProperty(indexed=True)
	version = db.StringProperty(indexed=True)
	last_updated = db.DateTimeProperty()
	author = db.StringProperty()
	cvs_users = db.StringListProperty()




	