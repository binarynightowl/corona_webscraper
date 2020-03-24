import scripts.sheets as gsheets
import json, urllib.request

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # use these APIs
cred_file = 'client-secret.json'  # client secret file, do not make this file public!
sheet_name = "COVID-19-CasesOverTime"  # what google sheet to use

# crappy code fix this later - maybe find a way to shorten urls if at all possible
world_url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/Coronavirus_2019_nCoV_Cases' \
            '/FeatureServer/1/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope' \
            '&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter' \
            '&returnGeodetic=false&outFields=*&returnGeometry=false&featureEncoding=esriDefault&multipatchOption' \
            '=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection' \
            '=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false' \
            '&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields' \
            '=&groupByFieldsForStatistics=&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C' \
            '%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22confirmed%22%7D%2C%7B' \
            '%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22deaths%22%2C%22outStatisticFieldName' \
            '%22%3A%22deaths%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22recovered' \
            '%22%2C%22outStatisticFieldName%22%3A%22recovered%22%7D%5D&having=&resultOffset=&resultRecordCount' \
            '=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat' \
            '=none&f=pjson&token= '
china_us_url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/ncov_cases/FeatureServer/2/query' \
               '?where=1%3D1&objectIds=18%2C4&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel' \
               '=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false' \
               '&outFields=+Country_Region%2C+confirmed%2C+deaths%2C+recovered%2C+active&returnGeometry=false' \
               '&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision' \
               '=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false' \
               '&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false' \
               '&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset' \
               '=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true' \
               '&quantizationParameters=&sqlFormat=none&f=pjson&token= '
state_url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/ncov_cases/FeatureServer/1/query' \
            '?where=Country_Region%3D%27US%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR' \
            '=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic' \
            '=false&outFields=Province_State%2C++confirmed%2C+deaths%2C+recovered%2C+active&returnGeometry=false' \
            '&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR' \
            '=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false' \
            '&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false' \
            '&cacheHint=true&orderByFields=confirmed&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset' \
            '=0&resultRecordCount=200&returnZ=false&returnM=false&returnExceededLimitFeatures=true' \
            '&quantizationParameters=&sqlFormat=none&f=pjson&token='


# get data for any state based on state name
def get_state_data(state_to_find):
    document = json.loads(urllib.request.urlopen(state_url).read().decode())['features']
    for state in document:
        state = state['attributes']
        if state['Province_State'] == state_to_find:
            return state['Confirmed']


# get data for all states in a given list and return it as a list
def get_all_state_data():
    states = ["New York", "Washington", "New Jersey", "California", "Illinois", "Michigan", "Florida", "Louisiana",
              "Massachusetts", "Texas", "Georgia", "Colorado"]
    values = []
    for state in states:
        values.append(get_state_data(state))
    return values  # there's gotta be a better way to do this but I am sleepy


# create a seperate sheets instance per workbook, by number
world = gsheets.Sheet(cred_file, scope, sheet_name, 1)
china = gsheets.Sheet(cred_file, scope, sheet_name, 2)
us = gsheets.Sheet(cred_file, scope, sheet_name, 3)

# scrape the data using a json search query and then read the appropriate information from the json document
data = json.loads(urllib.request.urlopen(world_url).read().decode())  # crappy code fix this later
total_cases = data['features'][0]['attributes']['confirmed']
total_deaths = data['features'][0]['attributes']['deaths']
total_recovered = data['features'][0]['attributes']['recovered']

# scrape more data using a json search query and then read the appropriate information from the json document
data = json.loads(urllib.request.urlopen(china_us_url).read().decode())  # crappy code fix this later
china_cases = data['features'][0]['attributes']['Confirmed']
china_deaths = data['features'][0]['attributes']['Deaths']
china_recovered = data['features'][0]['attributes']['Recovered']
us_cases = data['features'][1]['attributes']['Confirmed']
us_deaths = data['features'][1]['attributes']['Deaths']
us_recovered = data['features'][1]['attributes']['Recovered']

# # write the scraped data to the appropriate Google Sheets
world.write_data(total_cases, total_deaths, total_recovered)
china.write_data(china_cases, china_deaths, china_recovered)
us.write_data(us_cases, us_deaths, us_recovered)
us.write_state_data(get_all_state_data())  # crappy code fix this later

# cleanup / exit
print('Success!')
quit(0)
