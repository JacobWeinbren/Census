import ukcensusapi.Nomisweb as CensusApi
import urllib.request
import ujson
from pathlib import Path

loc = '../data/2011/'

def createPath(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def readMeta(table):
    #Read metadata
    api = CensusApi.Nomisweb("cache")
    meta = api.get_metadata(table)

    #Write metadata to file
    createPath(loc + table)
    with open(loc + table+ '/meta.json', 'w') as f:
        ujson.dump(meta, f)

    #Return metadata
    return meta

def findURL(meta, geo):

    """
    fields = meta['fields']

    #Find thing we are measuring
    fields.pop('nomis_table', None)
    fields.pop('description', None)
    fields.pop('fields', None)
    fields.pop('RURAL_URBAN', None)
    fields.pop('MEASURES', None)
    fields.pop('geographies', None)
    field = list(fields.keys())[0]

    values = [int(i) for i in meta['fields'][field].keys()]
    combined = str(min(values)) + '...' + str(max(values))
    """

    table_internal = meta['nomis_table']
    url = "https://www.nomisweb.co.uk/api/v01/dataset/" + table_internal + ".data.tsv?&MEASURES=20100&RURAL_URBAN=0&date=latest&geography=" + geo + "&select=GEOGRAPHY_CODE%2CCELL%2COBS_VALUE"
    return url

#Read list of tables
with open(loc + 'tables.txt', 'r') as f:
    tables = f.readlines()

#Write tables to files
for table in tables:
    print("Reading Meta")
    meta = readMeta(table)

    if meta:
        print("Reading Files for", table)

        #Create folder
        createPath(loc + table)

        #Output Area EW 2011
        url = findURL(meta, "2092957703TYPE299")
        urllib.request.urlretrieve(url, loc + table + '/output.tsv')

        #Output Areas Middle EW 2011
        url = findURL(meta, "2092957703TYPE297")
        urllib.request.urlretrieve(url, loc + table + '/lower.tsv')

        #Output Area District + Unitary EW 2011
        url = findURL(meta, "2092957703TYPE464")
        urllib.request.urlretrieve(url, loc + table + '/district.tsv')