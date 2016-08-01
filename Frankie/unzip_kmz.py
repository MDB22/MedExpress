import zipfile, os, pip, subprocess, glob, re, pymavlink, math
from lxml import etree
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX

def unzip_kmz(file_name):
	'Unzip the kmz file in the current directory'

	zip_ref = zipfile.ZipFile(file_name, 'r')
	contents = zip_ref.namelist()
	zip_ref.extractall("./kml_files")
	zip_ref.close()

	for file in contents:
		if file.endswith(".kml"):
			kml_file_name = file	#Kmz will only have one kml file

	rename_kml('kml_files/' + kml_file_name)

	return None

def rename_kml(file_name):
	'Rename kml files to allow us to easily see the most recent'
	current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
	os.rename(file_name, 'kml_files/mission_' + current_time + '.kml')

	return None


def parse_kml():
	'Parse the kml and obtain the coordinates'

	#All kml files are saved so grab the most recent one (we just unzipped the kmz to get it)
	file = get_most_recent_file()
	
	#Open the kml file ad obtain the longitude, latitude, and altitudes of the geofence
	with open(file, 'r') as f:
		root = ET.fromstring(f.read())

		kmlns = get_default_namespace(root)

		geofence = get_coords(root, kmlns, 'geofence')

		home_location= get_coords(root, kmlns, 'home')

		geofence_shrunk = shrink_geofence(geofence)

		make_kml_file(geofence_shrunk)
	
	return


def shrink_geofence(geofence):

	geo_len = len(geofence)
	shrunk_geofence = []

	for index in range(-1, geo_len - 2):
		if index == -1:
			lat_first = geofence[geo_len-2].lat
			lon_first = geofence[geo_len-2].lon
		else:
			lat_first = geofence[index].lat
			lon_first = geofence[index].lon

		lat_mid = geofence[index+1].lat
		lon_mid = geofence[index+1].lon
		lat_last = geofence[index+2].lat
		lon_last = geofence[index+2].lon

		distance_mid_to_start = distance_between(lat_mid,lon_mid,lat_first,lon_first)
		bearing_mid_to_start = bearing_between(lat_mid,lon_mid,lat_first,lon_first)

		distance_mid_to_last = distance_between(lat_mid,lon_mid,lat_last,lon_last)
		bearing_mid_to_last = bearing_between(lat_mid,lon_mid,lat_last,lon_last)

		step1 = get_new_gps_coord(geofence[0], bearing_mid_to_start, distance_mid_to_start*0.1)
		step2 = get_new_gps_coord(step1, bearing_mid_to_last, distance_mid_to_last*0.1)

		shrunk_geofence.append(step2)

	shrunk_geofence.append(shrunk_geofence[0])

	return shrunk_geofence


def make_kml_file(geofence):

	fld = KML.Folder()
	geometry_coords = []

	# create a KML file skeleton
	stylename = "sn_shaded_dot"
	doc = KML.kml(
		KML.Document(
			KML.Name("Sun Position"),
			KML.Style(
				KML.IconStyle(
					KML.scale(1.2),
					KML.Icon(
						KML.href("http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png")
					),
				),
				id=stylename,
			)
			KML.Folder(
				KML.name("Shrunk Geofence")
			)
		)
	)

	for coord in geofence:
		str_lat = str(coord.lat)
		str_lon = str(coord.lon)
		str_comb = "%s,%s,0 " % (str_lat,str_lon)
		geometry_coords.append(str_comb)


	geometry_string = ''.join(geometry_coords)

	doc.Document.Folder.append(KML.Placemark(
		KML.Polygon(
			KML.outerBoundaryIs(
				KML.linearRing(
					KML.coordinates(geometry_string)
				)
			)
		)
	))

	with open("./kml_modGeofence/Shrunk_Geofence.kml", "w") as text_file:
		text_file.write(etree.tostring(doc, pretty_print=True))



def get_new_gps_coord(original_location, bearing, distance_M):
	'Given original location, bearing and distance (in m) calculate new gps coords'
	R = 6378.137 #Radius of the Earth
	d_KM = distance_M/1000 #Distance in km

	bearing, lat1, lon1 = map(math.radians, [bearing, original_location.lat, original_location.lon])

	lat2 = math.asin( math.sin(lat1)*math.cos(d_KM/R) +
	     math.cos(lat1)*math.sin(d_KM/R)*math.cos(bearing))

	lon2 = lon1 + math.atan2(math.sin(bearing)*math.sin(d_KM/R)*math.cos(lat1),
	             math.cos(d_KM/R)-math.sin(lat1)*math.sin(lat2))

	lat2 = math.degrees(lat2)
	lon2 = math.degrees(lon2)

	return LocationGlobal(lat2,lon2,0)


def get_location_metres(original_location, dNorth, dEast):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`. The returned Location has the same `alt` value
    as `original_location`.
    """
    earth_radius=6378137.0 #Radius of "spherical" earth

    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt)


def distance_between(lat1_deg, lon1_deg, lat2_deg, lon2_deg):
	'Takes two coordinates in degrees and returns the distance between the two'
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(math.radians, [lon1_deg, lat1_deg, lon2_deg, lat2_deg])
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 

	# haversine formula 
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	c = 2 * math.asin(math.sqrt(a)) 
	dist_meters = (6367 * c)*1000

	return dist_meters


def bearing_between(lat1_deg, lon1_deg, lat2_deg, lon2_deg):
	'Take two coordinates in degrees and returns the compass bearing'
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(math.radians, [lon1_deg, lat1_deg, lon2_deg, lat2_deg])
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 

	#Bearing between the two points
	x = (math.sin(dlon) * math.cos(lat2))*1000
	y = ((math.cos(lat1) * math.sin(lat2)) - (math.sin(lat1)* math.cos(lat2) * math.cos(dlon)))*1000
	initial_bearing = math.atan2(x, y)
	initial_bearing = math.degrees(initial_bearing)

	#atan2 returns values from -180 to 180 which is not what we want for a compass
	compass_bearing = (initial_bearing + 360) % 360

	return compass_bearing


def get_default_namespace(kml_root):
	'Gets default namespace (schema it follows) of the kml document'
	return kml_root.tag.split('}')[0][1:]


def get_element(root_elem, def_namespace, element):
	'Find spefic elements that have root_elem as an ancestor (if there is a default namespace, that full URI gets prepended to all of the non-prefixed tags)'
	return root_elem.findall(".//{%s}%s" % (def_namespace, element))


def get_coords(kml_root, def_namespace, type):
	'Return the values of the kml tag most likely to contain the geofence'

	#Placemarks are features with associated geometry (ie point, polygon) that contain the different features of interest
	placemark_elems = get_element(kml_root, def_namespace, 'Placemark')

	coord_string = []
	names = []
	location = None

	for elem in placemark_elems:

		related_subelement = get_element(elem, def_namespace, kml_element_lookup(type))

		if related_subelement:

			#Get the name given to each placemark
			names.append(get_element(elem, def_namespace, 'name')[0].text)
			#Find all coordinate elements that are subelements of the most relevant tag
			coords = get_element(elem, def_namespace, 'coordinates')
			#Make sure coordinate string starts with the first longitude
			for coord in coords:
				m = re.search("\d", coord.text)
				coord_string.append(coord.text[m.start():])

	if type == 'geofence':
		location = get_geofence(coord_string)
	elif type == 'home':
		location = get_home_location(coord_string, names)

	return location


def get_home_location(coord_string, names):
	'Find the point coordinate corresponding to base location, and return the corresponding LocationGlobalRelative object'
	index = names.index('Base')
	home_location = coord_string[index]
	home_location = make_tidy_array(home_location)

	hl_longitude = home_location[0]
	hl_latitude = home_location[1]
	hl_altitude = home_location[2]

	return LocationGlobalRelative(hl_latitude, hl_longitude,hl_altitude)


def make_tidy_array(string_list):
	'Split the string of gps coords so each element is either a longitude, latitude, or altitude'
	array_split = re.split(r'[;,\s]\s*', string_list)
	array_split = filter(None, array_split)
	array_floats = [float(i) for i in array_split]
	return array_floats

def get_geofence(coord_string):
	'Find the longest coordnate string which should be the geofence, and return an array of LocationGlobalRelative objects'
	maxlength = max(len(s) for s in coord_string)
	geofence = [s for s in coord_string if len(s) == maxlength]
	geofence = make_tidy_array(geofence[0])

	geofence_object_arr = []

	geof_longitude = geofence[0::3]
	geof_latitude = geofence[1::3]
	geof_altitude = geofence[2::3]

	for index in range(len(geof_longitude)):
		geofence_object_arr.append(LocationGlobalRelative(geof_latitude[index],geof_longitude[index],geof_altitude[index]))

	return geofence_object_arr


def kml_element_lookup(key):
	'Lookup container element for different objects of interest (ie geofence or home location)'

	# Any geofence will be a Polygon element, a home location will be a single point
	dictionary = {
        'geofence': 'Polygon',
        'home': 'Point',
    }

	return dictionary[key]


def get_most_recent_file():
	'Return the most recently modified/created file'
	newest_file = max(glob.iglob('kml_files/*.kml'), key=os.path.getctime)
	return newest_file

#Frame format
# QGC WPL <VERSION>
# <INDEX> <CURRENT WP> <COORD FRAME> <COMMAND> <PARAM1> <PARAM2> <PARAM3> <PARAM4> <PARAM5/X/LONGITUDE> <PARAM6/Y/LATITUDE> <PARAM7/Z/ALTITUDE> <AUTOCONTINUE>

# Index -> What number command
# Current WP -> ??
# Coord Frame -> Essentially whether the altitude is absolute (measured from sea level) or relative to ground : 0 for absolute, 3 for relative
# Command -> What kind of message are we sending/receiving, ie. Waypoint, set paramater, ect.
# Param 1 -> Hold time in decimal seconds (Ignored by fixed wing)
# Param 2 -> Acceptance radius in meters (if the sphere with this radius is hit, the MISSION counts as reached)
# Param 3 -> 0 to pass through the WP, if > 0 radius in meters to pass by WP. Positive value for clockwise orbit, negative value for counter-clockwise orbit. Allows trajectory control.
# Param 4 -> Desired yaw angle at MISSION (rotary wing)
# Autocontinue -> Continue mission when reached

'''
http://gis.stackexchange.com/questions/8650/how-to-measure-the-accuracy-of-latitude-and-longitude/8674#8674
'''