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

OUTPUT_DIR = "../data/non-bts_images/"
NON_BTS_NODES = {
	"highway_residential": "\"highway\"=\"residential\"",
	"land_residential": "\"land\"=\"residential\"",
	"land_commercial": "\"land\"=\"commercial\"",
	"natural_water": "\"natural\"=\"water\"",
	"amenity_park": "\"amenity\"=\"parking_space\"",
	"bridge": "\"bridge\"=\"yes\""
}

if __name__ == '__main__':

	op = overpass.API(timeout=600)

	with open(args.area) as t:
		areas = t.readlines()
	ls_areas = [a.strip() for a in areas] 

	for boundary in ls_areas:
		for key, value in NON_BTS_NODES.items():
			print("Location: " + boundary + ". Searching for " + key + "...")
			bts = op.Get('area(' + str(boundary) + '); \
				(node[' + value + '](area);); \
				out;')

			bts_set = set(f.geometry.coordinates for f in bts.features)

			path = OUTPUT_DIR + boundary + "/" + key + "/"
			if not os.path.isdir(path):
				os.makedirs(path)

			if len(bts_set) == 0:
				print("Location: " + boundary + ". No " + key + " images.")
			else:
				print("Location: " + boundary +  ". Downloading " + str(len(bts_set)) + " " + key + " images...")
			for (lon, lat) in bts_set:
				SaveMapFromLatLon(lat, lon, args.apikey, path)
			
		print("Done. Image directory: " + OUTPUT_DIR + ".\n")