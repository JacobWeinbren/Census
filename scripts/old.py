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
    createPath(loc + 'tables/' + table)
    with open(loc + 'tables/' + table + '/meta.json', 'w') as f:
        ujson.dump(meta, f)

    #Return metadata
    return meta

def findURL(meta, geo):

    table_internal = meta['nomis_table']
    url = "https://www.nomisweb.co.uk/api/v01/dataset/" + table_internal + ".data.tsv?&MEASURES=20100&RURAL_URBAN=0&date=latest&geography=" + geo + "&select=GEOGRAPHY_CODE%2CCELL%2COBS_VALUE"
    return url

#Read list of tables
with open(loc + 'tables.txt', 'r') as f:
    tables = [i.replace("\n", "").strip() for i in f.readlines()]

#Write tables to files
for table in tables:
    print("Reading Meta")
    meta = readMeta(table)

    if meta:
        print("Reading Files for", table)

        #Create folder
        createPath(loc + 'tables/' + table)

        #Output Area EW 2011
        url = findURL(meta, "2092957703TYPE299")
        urllib.request.urlretrieve(url, loc + 'tables/' + table + '/oa.tsv')

        #Output Areas Middle EW 2011
        url = findURL(meta, "2092957703TYPE297")
        urllib.request.urlretrieve(url, loc + 'tables/' + table + '/msoa.tsv')

        #Output Area District + Unitary EW 2011
        url = findURL(meta, "2092957703TYPE464")
        urllib.request.urlretrieve(url, loc + 'tables/' + table + '/district.tsv')