
import json
import urllib2
from . import parser


#################
# USER FUNCTIONS
#################

# convenience methods for loading from different sources

def from_url(url, format=None):
    """
    Returns the crs object from a string interpreted as a specified format, located at a given url site.

    Arguments:
    - *url*: The url where the crs string is to be read from. 
    - *format*: Which format to parse the crs string as. One of "ogcwkt", "esriwkt", or "proj4", but also several others...

    Returns:
    - CRS object.
    """
    # first get string from url
    string = urllib2.urlopen(url).read()

    # then determine parser
    if format:
        # user specified format
        format = format.lower().replace(" ", "_")
        func = parser.__getattr__("from_%s" % format)
    else:
        # unknown format
        func = parser.from_unknown_text

    # then load
    crs = func(string)
    return crs

def from_file(filepath):
    """
    Returns the crs object from a file, with the format determined from the filename extension.
    """
    if filepath.endswith(".prj"):
        string = open(filepath, "r").read()
        return parser.from_esri_wkt(string)
    
    elif filepath.endswith((".geojson",".json")):
        raw = open(filepath).read()
        geoj = json.loads(raw)
        if "crs" in geoj:
            crsinfo = geoj["crs"]
            
            if crsinfo["type"] == "name":
                string = crsinfo["properties"]["name"]
                return parser.from_unknown_text(string)
                
            elif crsinfo["type"] == "link":
                url = crsinfo["properties"]["name"]
                type = crsinfo["properties"].get("type")
                return loader.from_url(url, format=type)
                
            else: raise Exception("invalid geojson crs type: must be either name or link")

        else:
            # assume default wgs84 as per the spec
            return parser.from_epsg_code("4326")

##    elif filepath.endswith((".tif",".tiff",".geotiff")):
##        pass
##        # ...




                                      
        
