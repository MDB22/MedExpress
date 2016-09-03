from softgeofence import get_geofence, modify_geofence, LocationGlobal

geofence = get_geofence('sample_mission.kmz')
shrunken_geofence = modify_geofence(geofence, 100, create_kml=True, shrink = True)

if shrunken_geofence.is_coord_inside(location = LocationGlobal(-27.32791, 151.37503)):
	print "Inside fence"
else:
	print "Outside fence"

if geofence.is_coord_inside(location = LocationGlobal(-27.32791, 151.37503)):
	print "Inside fence"
else:
	print "Outside fence"


