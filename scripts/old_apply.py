import ujson, copy, os, csv
from fastnumbers import fast_real
import time
from datetime import timedelta

#Get data from Tables
def getTableData(zoom_level):

    #Get all folders in table storage
    folders = [i[0] for i in os.walk('../data/2011/tables')]
    table_data = []

    #Read folders
    for folder in folders[1:]:

        #Read tsv file from folder
        with open(folder + '/meta.json') as meta_file:
            meta = ujson.load(meta_file)
    
        #Read tsv file from folder
        with open(folder + '/' + zoom_level + '.tsv') as tsv:

            folder_name = folder.split('/')[-1]
            
            table_data.append((
                folder_name, 
                list(csv.DictReader(tsv, delimiter = '\t')),
                meta
            ))

    return table_data

#Applies table data to map
def applyData(geojson_file, zoom_level, identifier, out_file):

    print("Reading", geojson_file)
    
    #Open File
    with open(geojson_file) as f:
        geojson = ujson.load(f)

    #To iterate over
    geojson_copy = copy.deepcopy(geojson)

    #Timer
    starting_time = time.time()

    table_data = getTableData(zoom_level)

    #For all features
    for index, feature in enumerate(geojson_copy['features']):

        #Get feature name
        name = feature['properties'][identifier]

        #Clear properties
        geojson['features'][index]['properties'] = {}

        #Compare with table data
        for table in table_data:

            folder_name = table[0]
            data = table[1] 

            #Iterate table rows
            for row in data:

                row_name = row['GEOGRAPHY_CODE']

                #If match
                if name == row_name:

                    #Store properties into feature
                    if not folder_name in geojson['features'][index]['properties']:
                        geojson['features'][index]['properties'][folder_name] = {}
                    
                    geojson['features'][index]['properties'][folder_name][row['CELL']] = fast_real(row['OBS_VALUE'])

        if index % 100 == 0:
            print(index)
            ending_time = time.time()
            print(timedelta(seconds=ending_time - starting_time))
            starting_time = time.time()

    #Store file
    with open(out_file, 'w') as f:
	    ujson.dump(geojson, f)

if __name__ == "__main__":
    #Districts / Authorities
    applyData('../data/2011/maps/authorities.geojson', 'district', 'lad11cd', '../data/2011/maps/authorities_data.geojson')

    #MSOA
    applyData('../data/2011/maps/msoa.geojson', 'msoa', 'MSOA01CD', '../data/2011/maps/msoa_data.geojson')

    #OA
    applyData('../data/2011/maps/oa.geojson', 'oa', 'OA11CD', '../data/2011/maps/oa_data.geojson')
