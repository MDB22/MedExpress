from zipfile import PyZipFile
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

# Processes a KMZ file and returns a dictionary of important points/landmarks
## TODO: Improve robustness, ideally shouldn't depend on knowing the Placemark names
def GenerateMission(filename):

    # Create XML parser
    parser = make_parser()
    generator = MissionGenerator()
    parser.setContentHandler(generator)

    # Parse KMZ file
    kmz = PyZipFile(filename, 'r')
    kml = kmz.open('doc.kml', 'r')
    parser.parse(kml)

    kmz.close()

    # Arrange the XML items into useful variables
    items = {}
    items['base_location'] = ParseCoordinates(generator.mapping, 'Base')
    items['landing_site'] = ParseCoordinates(generator.mapping, 'Fake reported location')
    items['base_geofence'] = ParseCoordinates(generator.mapping, 'Base geofence')
    items['landing_site_geofence'] = ParseCoordinates(generator.mapping, 'Sample remote landing site')
    items['mission_geofence'] = ParseCoordinates(generator.mapping, 'Sample full geofence')
    items['path'] = ParseCoordinates(generator.mapping, 'Sample Nominal Path')
    
    return items

# Converts the stirng of coordinate positions to a list of tuples,
# arranged as (lat, long, alt)
def ParseCoordinates(mapping, item):

    coordinates = mapping[item]['coordinates'].split()

    coords_list = []
    location = {}
    
    for c in coordinates:
        items = c.split(',')
        location['lat'] = float(items[1])
        location['long'] = float(items[0])
        location['alt'] = float(items[2])
        coords_list.append(location)

    return coords_list

# Class for dealing with XML data and processing KMZ file
class MissionGenerator(ContentHandler):

    def __init__(self):
        self.inName = False # handle XML parser events
        self.inPlacemark = False
        self.mapping = {} 
        self.buffer = ""
        self.name_tag = ""
        
    def startElement(self, name, attributes):
        if name == "Placemark": # on start Placemark tag
            self.inPlacemark = True
            self.buffer = "" 
        if self.inPlacemark:
            if name == "name": # on start title tag
                self.inName = True # save name text to follow
            
    def characters(self, data):
        if self.inPlacemark: # on text within tag
            self.buffer += data # save text if in title
            
    def endElement(self, name):
        self.buffer = self.buffer.strip('\n\t')
        
        if name == "Placemark":
            self.inPlacemark = False
            self.name_tag = "" #clear current name
        
        elif name == "name" and self.inPlacemark:
            self.inName = False # on end title tag            
            self.name_tag = self.buffer.strip()
            self.mapping[self.name_tag] = {}
        elif self.inPlacemark:
            if name in self.mapping[self.name_tag]:
                self.mapping[self.name_tag][name] += self.buffer
            else:
                self.mapping[self.name_tag][name] = self.buffer
        self.buffer = ""
