#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Processes the apt - airports file"""
import sys
#import csv
#import yaml
import json
in_file_name = "/home/flight-sim/public_html/flightgear-php/CVS/data/Airports/apt.dat"
#airports_csv = "../prepared_data/airports.csv"
#airports_yaml = "../fg_data_app/yaml/airports.yaml"

"""
class Airport(db.Model):
	icao = db.StringProperty()
	name = db.StringProperty()
	heliport = db.BooleanProperty()
	seaport = db.BooleanProperty()
	elevation = db.IntegerProperty()
	atc = db.BooleanProperty()
"""


class ProcessAirports:

	col_map = {'key':0, 'elevation':1, 'atc':2, '_':3, 'icao':4, 'name':5}
	nos = ['0', '1','2','3','4','5','6','7','8','9']

	def is_icao(self, code):
		if len(code) != 4:
			return False
		for n in self.nos:
			if code.find(n) > -1:
				return False
		return True

	def __init__(self, in_file_name):
		self.in_file = open(in_file_name)

		#self.airports_csv = csv.writer(open(airports_csv, 'w'), quoting=csv.QUOTE_ALL)
		#self.airports_yaml = open(airports_yaml, 'w')
		# skip first three lines
		self.read_line()
		self.read_line()
		self.read_line()

		self.airports = {}
		c = 0
		
		while 1:
			line =  self.in_file.readline()
			if not line:
				self.process_items()
				return
				##self.close()
				#return None
			line = line.strip()
			if line:
				cols = line.split()
				## aiport, seaplane, heliport
				akey = cols[0]
				
				heliports = []
				seaports = []
				if akey != '99':
					if akey in ['1', '16', '17']:
						seaport = True if akey == '16' else False
						heliport = True if akey == '17' else False
						#                            icoa,    name,    seaport, heliport, elev,    atc
						#print cols
						airport_raw = " ".join(cols[5:])
						icao = str(cols[4])
						is_valid = self.is_icao(icao)
						if self.is_icao(icao):
							#self.airports_csv.writerow( [cols[4], airport, seaport, heliport, cols[1], cols[2]] )

							bits = str(airport_raw)
							airport = ''
							#print "...........", airport
							for b in bits:
								try:
									json.dumps({'foo': b})
									airport += b
								except:
									pass

							"""
							self.airports[icao] = { 
									'name': airport, 
									'seaport': seaport, 
									'heliport': heliport,
									'elevation': int(cols[1]),
									'atc': bool(cols[2])
							}
							"""
							self.airports[icao] =  icao + ' ' + airport.replace("'", "")
									
							#print self.airports[icao]
							#json.dumps(self.airports[icao])
						#else:
							#print 'skip', icao
						#yaml.dump(yam, self.airports_yaml, width=500, indent=4)
						if c % 500 == 0:
							print c, cols[4] #, airport
				
						if c == 500:
							print "break"
							#self.process_items()
							#return
						c += 1

	def process_items(self):
		sorted_airports = sorted(self.airports.keys())
		#print "ALL+", len(sorted_airports)
		f = open('../ffs-schedule.appspot.com/data/airports.py', 'w')
		f.write("airports = {}\n")
		data = []
		for ki in sorted_airports:
			data.append({'icao': ki, 'airport': self.airports[ki]})
			s = "airports['%s'] = '%s'\n" % (ki, self.airports[ki])
			f.write( s )
		f.write( "\n")
		f.close()
		print "### done ####", #c
		#self.close()

	def read_line(self):
		line =  self.in_file.readline()
		if not line:
			print "End of file flag reached"
			##self.close()
			return None
		return line.strip()

	def close(self):
		self.in_file.close()

		

d = ProcessAirports(in_file_name)
