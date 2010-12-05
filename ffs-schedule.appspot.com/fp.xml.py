#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from BeautifulSoup.BeautifulSoup import BeautifulSoup
#import xml.dom.minidom
"""
<PropertyList>

	<departure>
		<airport>KBWI</airport>
	</departure>

	<destination>
		<airport>KMCI</airport>
	</destination>

	<cruise>
		<altitude-ft>50000</altitude-ft>
	</cruise>

	<route>
		<wp>
			<altitude-ft>3000</altitude-ft>
			<latitude-deg>39.2253</latitude-deg>
			<longitude-deg>-76.939</longitude-deg>
			<ident>TERPZ</ident>
		</wp>


"""
file_name = './data/plans/KSLC-KMCI.xml'

f = open(file_name, 'r')
xml = f.read()

#try:
#	doc = xml.dom.minidom.parseString(xml)
#except :
#	print "ERRORsome parse error"

soup = BeautifulSoup(xml)
#dep = BeautifulSoup(xml).findAll("departure")
#print dep	
		
pilots = {}		
atc = {}
player_ips = {}
#servers_lookup = server_ip_lookup()

#for node in doc.getElementsByTagName("departure"):
	#print node
	
dic = {}
dic['dep'] = soup.departure.airport.text
dic['arr'] = soup.destination.airport.text
dic['cruise'] = soup.cruise.findAll("altitude-ft")[0].text
dic['route'] = []
wp = soup.route.findAll("wp")
for w in wp:
	dic['route'].append({'ident': w.ident.text})

print dic