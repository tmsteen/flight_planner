#Import necesary mdules
import urllib2
from BeautifulSoup import BeautifulSoup
import requests

#Get origin from user
origin = raw_input("What is your origin? ")

#Got to FAA page to gather airport data
soup = BeautifulSoup(requests.get("https://nfdc.faa.gov/nfdcApps/services/airportLookup/airportDisplay.jsp?airportId={0}".format(origin)).text)

tableSummary = soup.find('table', {'class' : 'table table-condensed table-borderless' })

for row in tableSummary:
	if "Latitude" in str(row):
		elements = row.findAll("td")
		print elements[1].text
