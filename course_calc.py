#Import necesary mdules
#import urllib2
from BeautifulSoup import BeautifulSoup
import requests
import re
import LatLon23
import sys

def get_lat_lon(origin):
	#Got to FAA page to gather airport data
	soup = BeautifulSoup(requests.get("https://nfdc.faa.gov/nfdcApps/services/airportLookup/airportDisplay.jsp?airportId={0}".format(origin)).text)
	
	#Get the pertinent section of the page
	tableSummary = soup.find('table', {'class' : 'table table-condensed table-borderless' })

	#Regex for coordinates format
	lat_regex = '\d{1,2}-\d{1,2}-\d{1,2}.\d{1,} [N,S]'
	lon_regex = '\d{1,2}-\d{1,2}-\d{1,2}.\d{1,} [E,W]'

	#Iterate through the data on the page and pull the coords
	for row in tableSummary:
		if "Latitude" in str(row):
			#narrows down to specific element and strings it
			elements = str(row.findAll("td")[1].text)
			lat = re.search(lat_regex, elements)
			lon = re.search(lon_regex, elements)

	#group refers to the found items from the regex above
	coords = LatLon23.string2latlon(lat.group(0), lon.group(0), 'd%-%m%-%S% %H')

	return coords

def course(origin, dest):
	#Converstion for miles (native output is KM)
	distance = origin.distance(dest) * 0.539957
	heading = origin.heading_initial(dest)

	#correct for negative westerly headings
	if heading < 0:
		heading = 360 + heading

	print "Course: {0:.0f} Degrees \t Distance: {1:.2f} nm".format(heading, distance)

	return distance, heading


#Get user input
user_origin = raw_input("What is your origin? ")
user_destination = raw_input("What is your destination? ")

#Compute coords
try:
	origin_coords = get_lat_lon(user_origin)
	dest_coords = get_lat_lon(user_destination)
except TypeError:
	print "ICAO does not exist...try with/without 'K' prefix.  The FAA website does not use a 'K' for smaller airports. \n Exitting..."
	sys.exit()

#Determine course
course(origin_coords, dest_coords)

