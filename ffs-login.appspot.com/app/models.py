# -*- coding: utf-8 -*-
from google.appengine.ext import db

"""
The Data Definition
"""

class Comment(db.Model):
	comment =  db.StringProperty(multiline=True)
	section = db.StringProperty(indexed=True)
	#section = db.StringProperty(indexed=True)
	dated = db.DateTimeProperty(indexed=True, auto_now_add=True)
	author = db.UserProperty()
	




	