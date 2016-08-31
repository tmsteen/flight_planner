#Import necesary mdules
import urllib2
from BeautifulSoup import BeautifulSoup
import requests
import re

def get_lat_long(origin):
	#Get origin from user
	#origin = raw_input("What is your origin? ")

	#Got to FAA page to gather airport data
	#soup = BeautifulSoup(requests.get("https://nfdc.faa.gov/nfdcApps/services/airportLookup/airportDisplay.jsp?airportId={0}".format(origin)).text)
	#test
	soup = BeautifulSoup(requests.get("https://nfdc.faa.gov/nfdcApps/services/airportLookup/airportDisplay.jsp?airportId=KCVB").text)

	tableSummary = soup.find('table', {'class' : 'table table-condensed table-borderless' })

	lat_regex = '([0-9]{1,2}-[0-9]{1,2}-[0-9]{1,2}.[0-9]) [N,S]'
	lon_regex = '([0-9]{1,2}-[0-9]{1,2}-[0-9]{1,2}.[0-9]) [E,W]'

	for row in tableSummary:
		if "Latitude" in str(row):
			elements = str(row.findAll("td")[1].text)
			lat = re.search(lat_regex, elements)
			lon = re.search(lon_regex, elements)

return lat, lon

