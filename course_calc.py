#Import necesary mdules
import urllib2
from BeautifulSoup import BeautifulSoup
import requests
import re
import LatLon

def get_lat_lon(origin):
	#Get origin from user
	#origin = raw_input("What is your origin? ")

	#Got to FAA page to gather airport data
	soup = BeautifulSoup(requests.get("https://nfdc.faa.gov/nfdcApps/services/airportLookup/airportDisplay.jsp?airportId={0}".format(origin)).text)

	tableSummary = soup.find('table', {'class' : 'table table-condensed table-borderless' })

	lat_regex = '([0-9]{1,2}-[0-9]{1,2}-[0-9]{1,2}.[0-9]{1-3}) [N,S]'
	lon_regex = '([0-9]{1,2}-[0-9]{1,2}-[0-9]{1,2}.[0-9]{1-3}) [E,W]'

	for row in tableSummary:
		if "Latitude" in str(row):
			elements = str(row.findAll("td")[1].text)
			lat = re.search(lat_regex, elements)
			lon = re.search(lon_regex, elements)

	#print lat.group()
	#print lon.group()

	coords = LatLon.string2latlon(lat.group(), lon.group(), 'd%-%m%-%S% %H')

	#print "Coords: {0}".format(coords)

	return coords

def course(origin, dest):
	distance = origin.distance(dest) * 0.539957
	heading = origin.heading_initial(dest)

	print "Course: {0:.0f} Degrees \t Distance: {1:.2f} nm".format(heading, distance)

	return distance, heading

origin_coords = get_lat_lon('KCVB')
dest_coords = get_lat_lon('49R')

course(origin_coords, dest_coords)

