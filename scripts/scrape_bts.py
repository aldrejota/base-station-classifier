import argparse
import overpass
from gmaps_wrapper import SaveMapFromLatLon
import os

parser = argparse.ArgumentParser(description='Scrape Images of Base Transceiver Stations')
parser.add_argument('--area', action='store',
                    dest='area',
                    const=None,
                    required=True,
                    help='File containing newline-delimited areas (OSM boundaries).')
parser.add_argument('--apikey', action='store',
                    dest='apikey',
                    const=None,
                    required=True,
                    help='Google Static Maps API Key.')
args = parser.parse_args()

OUTPUT_DIR = "../data/bts_images/"

if __name__ == '__main__':

	op = overpass.API(timeout=600)

	with open(args.area) as t:
		areas = t.readlines()
	ls_areas = [a.strip() for a in areas] 

	for boundary in ls_areas:
		
		print("Location: " + boundary + ". Searching for BTS...")
		bts = op.Get('area(' + str(boundary) + '); \
			(node["tower:type"="communication"]["communication:mobile_phone"="yes"](area);); \
			out;')
		
		bts_set = set(f.geometry.coordinates for f in bts.features)

		path = OUTPUT_DIR + boundary + "/"
		if not os.path.isdir(path):
			os.makedirs(path)

		print("Location: " + boundary +  ". Downloading BTS images...")
		for (lon, lat) in bts_set:
			SaveMapFromLatLon(lat, lon, args.apikey, path)
		
	print("Done. Image directory: " + OUTPUT_DIR + ".\n")