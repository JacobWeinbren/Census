import ujson, math, statistics
from old_apply import getTableData
from fastnumbers import fast_real

#https://www.highcharts.com/blog/tutorials/data-science-and-highcharts-kernel-density-estimation/
def GaussKDE(xi, x):
    return (1 / math.sqrt(2 * math.pi)) * math.exp(math.pow(xi - x, 2) / -2);

#See above
def densityPlot(raw_data):
    xiData = []
    data_range = max(raw_data) - min(raw_data)
    startPoint = min(raw_data)
    for i in range(int(data_range)):
        xiData.append(startPoint + i)
    
    data = []
    N = len(raw_data)

    for item in xiData:
        temp = 0
        for j in range(N):
            temp = temp + GaussKDE(item, raw_data[j]);
        data.append([item, (1 / N) * temp]);

    return data

#Table Data
oa_tables = getTableData('oa')

data = {}

#Open File
print ("Reading file")
with open('../data/2011/maps/oa.geojson') as f:
    geojson = ujson.load(f)

print ("Scanning districts")
districts = {}
for feature in geojson['features']:
    districts[feature['properties']['OA11CD']] = feature['properties']['LAD11CD']

#Iterate all tables
for index, table in enumerate(oa_tables):

    table_name = table[0]
    oa_data = table[1]
    meta = table[2]

    print("Reading", table_name)

    data[table_name] = {}

    fields = meta['fields']

    #Get all fields in table
    fields.pop('nomis_table', None)
    fields.pop('description', None)
    fields.pop('fields', None)
    fields.pop('RURAL_URBAN', None)
    fields.pop('MEASURES', None)
    fields.pop('geographies', None)
    fields.pop('GEOGRAPHY', None)
    #Accessor
    field = list(fields.keys())[0]

    #Get all field ids
    values = fields[field]

    #Extract raw data
    for item in oa_data:

        cell = item['CELL']

        if not cell in data[table_name]:

            #Write the name to data
            data[table_name][cell] = {}
            data[table_name][cell]['raw_values'] = []
            data[table_name][cell]['district_values'] = {}
            data[table_name][cell]['district_data'] = {}

        #Add in to all values (EW)
        obs_value = item['OBS_VALUE']
        data[table_name][cell]['raw_values'].append(fast_real(obs_value))

        #Add to District
        district = districts[item['GEOGRAPHY_CODE']] 

        if district not in data[table_name][cell]['district_values']:
            data[table_name][cell]['district_values'][district] = []
            data[table_name][cell]['district_data'] = {}

        data[table_name][cell]['district_values'][district].append(fast_real(obs_value))

    for cell in data[table_name]:
        
        #Orders for curve fitting
        raw_values = data[table_name][cell]['raw_values']
        raw_values.sort()

        #Loads in curve fitting
        raw_density = densityPlot(raw_values)
        data[table_name][cell].pop('raw_values', None)
        data[table_name][cell]['density'] = raw_density
        data[table_name][cell]['median'] = statistics.median(raw_values)

        #Loads in district data
        for district in data[table_name][cell]['district_values']: 

            #Orders in curve fitting
            district_values = data[table_name][cell]['district_values'][district]
            district_values.sort()
            district_density = densityPlot(data[table_name][cell]['district_values'][district])
            median = statistics.median(data[table_name][cell]['district_values'][district])

            #Loads in curve fitting
            data[table_name][cell]['district_data'][district] = {}
            data[table_name][cell]['district_data'][district]['density'] = district_density
            data[table_name][cell]['district_data'][district]['median'] = median

        data[table_name][cell].pop('district_values', None)

with open('../data/2011/2011.json', 'w') as f:
	ujson.dump(data, f)
            

    

    

    

