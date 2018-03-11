"""This module contains 3 geojson objects.
geo_regions
geo_LAs
geo_london
"""

from lds.data import Data
import json
import urllib.request

df = Data["Travel_2011"]

LAtoRegion = {LA:region for LA,region in zip(df["LA"],df["Region"])}
LAs = df["LA"].tolist()
london_LAs = [LA for LA in LAtoRegion if LAtoRegion[LA] == "London"]

region_clean = {'East Midlands (England)': 'East Midlands',
                'North East (England)': 'North East',
                'North West (England)': 'North West',
                'South East (England)': 'South East',
                'South West (England)': 'South West',
                'West Midlands (England)': 'West Midlands',
                'London': 'London',
                'Wales': 'Wales',
                'Yorkshire and The Humber': 'Yorkshire and The Humber',
                'East of England': 'East of England'        
               }



# This code gives us the geojson for regions    
URL = urllib.request.urlopen('http://geoportal1-ons.opendata.arcgis.com/datasets/01fd6b2d7600446d8af768005992f76a_4.geojson').read()
geo_regions = json.loads(URL)
geo_regions['features'] = [region for region in geo_regions['features'] if region["properties"]["nuts118nm"] in region_clean]

for region in geo_regions['features']:
    region["properties"]["name"] = region_clean[region["properties"].pop("nuts118nm")]
    # change the property to name rather than nuts118nm


# This code gives us the geojson for LAs   
URL = urllib.request.urlopen('https://opendata.arcgis.com/datasets/5e14c6bedc8740d19683517e5e902057_0.geojson').read()
geo_LAs = json.loads(URL)

geo_LAs['features'] = [LA for LA in geo_LAs['features'] if LA["properties"]["lad09nm"] in LAs]

for LA in geo_LAs['features']:
    LA["properties"]["name"] = LA["properties"].pop("lad09nm")
    LA["properties"]["region"] = LAtoRegion[LA["properties"]["name"]]


# This code gives us the geojson for London LAs  
geo_london = geo_LAs.copy()
geo_london["features"] = [LA for LA in geo_london["features"] if LA["properties"]["name"] in london_LAs]

