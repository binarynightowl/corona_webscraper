import scripts.sheets as gsheets
from covid19_data import JHU
import covid19_data
from threading import Thread

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # use these APIs
cred_file = 'client-secret.json'  # client secret file, do not make this file public!
sheet_name = "COVID-19-CasesOverTime"  # what google sheet to use

state_data = {
}


# get data for any state based on state name and put it in state_data (dict)
def get_state_data(state_to_find):
    state = covid19_data.dataByNameShort(state_to_find)
    state_data[state_to_find] = (state.confirmed - state.deaths - state.recovered)


# get data for all states in a given list and store it to a dictionary
def get_all_state_data():
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'DistrictofColumbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'NorthCarolina',
        'ND': 'NorthDakota',
        'NE': 'Nebraska',
        'NH': 'NewHampshire',
        'NJ': 'NewJersey',
        'NM': 'NewMexico',
        'NV': 'Nevada',
        'NY': 'NewYork',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'RhodeIsland',
        'SC': 'SouthCarolina',
        'SD': 'SouthDakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'WestVirginia',
        'WY': 'Wyoming'
    }
    for state in states:
        get_state_data(state)


def write_world_data():
    world_sheet = gsheets.Sheet(cred_file, scope, sheet_name, 1)
    total = JHU.Total
    world_sheet.write_data(total.cases, total.deaths, total.recovered)


def write_china_data():
    china_sheet = gsheets.Sheet(cred_file, scope, sheet_name, 2)
    china = JHU.China
    china_sheet.write_data(china.cases, china.deaths, china.recovered)


def write_us_data():
    us_sheet = gsheets.Sheet(cred_file, scope, sheet_name, 3, state_data)
    us = JHU.US
    get_all_state_data()
    us_sheet.write_data(us.cases, us.deaths, us.recovered, state_data)
    # us_sheet.write_state_data(state_data)


def write_all_data():
    t1 = Thread(target=write_world_data)
    t2 = Thread(target=write_china_data)
    t3 = Thread(target=write_us_data)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


write_all_data()
# cleanup / exit
quit(0)
