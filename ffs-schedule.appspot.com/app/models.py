# -*- coding: utf-8 -*-
from google.appengine.ext import db

"""
The Data Definition
"""

class Comment(db.Model):
	comment =  db.StringProperty(multiline=True)
	section = db.StringProperty(indexed=True)
	dated = db.DateTimeProperty(indexed=True, auto_now_add=True)
	author = db.UserProperty()


class Cookie(db.Model):
	sessID =  db.StringProperty(indexed=True)
	dated = db.DateTimeProperty(indexed=True, auto_now_add=True)

class FPp(db.Model):
	cookie = db.StringProperty(indexed=True)
	callsign = db.StringProperty(indexed=True, required=True)
	dep =  db.StringProperty(indexed=True)
	dep_date = db.DateTimeProperty(indexed=True)
	dep_atc =  db.StringProperty(indexed=True)
	arr =  db.StringProperty(indexed=True)
	arr_date = db.DateTimeProperty(indexed=True)
	arr_atc =  db.StringProperty(indexed=True)
	comment =  db.StringProperty(multiline=True)
	email = db.StringProperty()



	