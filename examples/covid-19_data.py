"""
This example shows how to get just the COVID-19 data from the John Hopkins University if you would like to use the
data in your application for other purposes
"""

import json, urllib.request

# query to get the total of all the confirmed cases, deaths, and recovered cases in the world - check GitHub for more
# info
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
# query to get the cases, deaths, and recovered cases in the US and China - check GitHub for more info
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
# query to get the cases, deaths, and recovered cases in every State - check GitHub for more info
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


# find data for any state based on state name EX: Texas
def get_state_data(state_to_find):
    document = json.loads(urllib.request.urlopen(state_url).read().decode())['features']
    for state in document:
        state = state['attributes']
        if state['Province_State'] == state_to_find:
            return state['Confirmed']


data = json.loads(urllib.request.urlopen(world_url).read().decode())  # scrape data from JSON Query

total_cases = data['features'][0]['attributes']['confirmed']
total_deaths = data['features'][0]['attributes']['deaths']
total_recovered = data['features'][0]['attributes']['recovered']
total = [total_cases, total_deaths, total_recovered]

data = json.loads(urllib.request.urlopen(china_us_url).read().decode())  # scrape data from new JSON Query

china_cases = data['features'][0]['attributes']['Confirmed']
china_deaths = data['features'][0]['attributes']['Deaths']
china_recovered = data['features'][0]['attributes']['Recovered']
china = [china_cases, china_deaths, china_recovered]

us_cases = data['features'][1]['attributes']['Confirmed']
us_deaths = data['features'][1]['attributes']['Deaths']
us_recovered = data['features'][1]['attributes']['Recovered']
us = [us_cases, us_deaths, us_recovered]

texas = get_state_data("Texas")  # example:Texas - you should be able to get all 60 states/territories with this

print(total, china, us, texas)
