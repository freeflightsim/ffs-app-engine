# -*- coding: utf-8 -*-

DEBUG = True


APP_ID = 'ffs-cal'

tm = "<span class='tm'>FreeFlightSim</span>" #&#0174;

SITE_TITLE = "FlightGear calendar at FreeFlightSim.org"
SITE_HEADER = "Free Flight Simulation"

GOOGLE_PROJECT = "freeflightsim"
ISSUES_FEED = 'http://code.google.com/feeds/issues/p/freeflightsim/issues/full'


#MP_STATUS_URL = "http://mpmap01.flightgear.org/mpstatus/"
#MP_PILOTS_URL = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"

CDN = 'http://ffs-cache.appspot.com'
#CDN = ''

##########################################################
## Langs - TODO add links
##########################################################
langs = [ 	{'code': 'En', 'label': 'English'},
			{'code': 'Fi', 'label': 'French'},
			{'code': 'Es', 'label': 'Spanish'},
			{'code': 'De', 'label': 'German'}
]

EMAIL = 'fg@freeflightsim.org'
SECRET = 'secret'

CAL_URL = 'http://www.google.com/calendar/render?cid=%s' % EMAIL