import json
import scripts.sheets as gsheets
from covid19_data import JHU
import covid19_data
from threading import Thread
import os

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # use these APIs
cred_file = os.environ['secret']  # client secret file, do not make this file public!
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
    world_sheet = gsheets.Sheet(cred_file, scope, sheet_name, 'World')
    total = JHU.Total
    world_sheet.write_data(total.cases, total.deaths, total.recovered)


def write_china_data():
    china_sheet = gsheets.Sheet(cred_file, scope, sheet_name, 'China')
    china = JHU.China
    china_sheet.write_data(china.cases, china.deaths, china.recovered)


def write_us_data():
    us_sheet = gsheets.Sheet(cred_file, scope, sheet_name, 'US', state_data)
    us = JHU.US
    get_all_state_data()
    us_sheet.write_data(us.cases, us.deaths, us.recovered, state_data)


def write_countries_data():
    countries = ['AUSTRALIA',
                 'AUSTRIA',
                 'CANADA',
                 'CHINA',
                 'DENMARK',
                 'FINLAND',
                 'FRANCE',
                 'GERMANY',
                 'ICELAND',
                 'IRELAND',
                 'ITALY',
                 'NETHERLANDS',
                 'NORWAY',
                 'RUSSIA',
                 'SWEDEN',
                 'SWITZERLAND',
                 'UNITEDKINGDOM',
                 'US',
                 'SPAIN',
                 'MEXICO',
                 'CHILE',
                 'BRAZIL',
                 'PERU',
                 'COLOMBIA',
                 'JAPAN',
                 'UKRAINE',
                 'INDIA',
                 'PAKISTAN',
                 'AFGHANISTAN',
                 'ALBANIA',
                 'ALGERIA',
                 'ANDORRA',
                 'ANGOLA',
                 'ANTIGUAANDBARBUDA',
                 'ARGENTINA',
                 'ARMENIA',
                 'AZERBAIJAN',
                 'BAHAMAS',
                 'BAHRAIN',
                 'BANGLADESH',
                 'BARBADOS',
                 'BELARUS',
                 'BELGIUM',
                 'BELIZE',
                 'BENIN',
                 'BHUTAN',
                 'BOLIVIA',
                 'BOSNIAANDHERZEGOVINA',
                 'BOTSWANA',
                 'BRUNEI',
                 'BULGARIA',
                 'BURKINAFASO',
                 'BURMA',
                 'BURUNDI',
                 'CABOVERDE',
                 'CAMBODIA',
                 'CAMEROON',
                 'CENTRALAFRICANREPUBLIC',
                 'CHAD',
                 'COMOROS',
                 'CONGOBRAZZAVILLE',
                 'CONGOKINSHASA',
                 'COSTARICA',
                 'COTEDIVOIRE',
                 'CROATIA',
                 'CUBA',
                 'CYPRUS',
                 'CZECHIA',
                 'DIAMONDPRINCESS',
                 'DJIBOUTI',
                 'DOMINICA',
                 'DOMINICANREPUBLIC',
                 'ECUADOR',
                 'EGYPT',
                 'ELSALVADOR',
                 'EQUATORIALGUINEA',
                 'ERITREA',
                 'ESTONIA',
                 'ESWATINI',
                 'ETHIOPIA',
                 'FIJI',
                 'GABON',
                 'GAMBIA',
                 'GEORGIA',
                 'GHANA',
                 'GREECE',
                 'GRENADA',
                 'GUATEMALA',
                 'GUINEA',
                 'GUINEABISSAU',
                 'GUYANA',
                 'HAITI',
                 'HOLYSEE',
                 'HONDURAS',
                 'HUNGARY',
                 'INDONESIA',
                 'IRAN',
                 'IRAQ',
                 'ISRAEL',
                 'JAMAICA',
                 'JORDAN',
                 'KAZAKHSTAN',
                 'KENYA',
                 'KOREASOUTH',
                 'KOSOVO',
                 'KUWAIT',
                 'KYRGYZSTAN',
                 'LAOS',
                 'LATVIA',
                 'LEBANON',
                 'LESOTHO',
                 'LIBERIA',
                 'LIBYA',
                 'LIECHTENSTEIN',
                 'LITHUANIA',
                 'LUXEMBOURG',
                 'MSZAANDAM',
                 'MADAGASCAR',
                 'MALAWI',
                 'MALAYSIA',
                 'MALDIVES',
                 'MALI',
                 'MALTA',
                 'MAURITANIA',
                 'MAURITIUS',
                 'MOLDOVA',
                 'MONACO',
                 'MONGOLIA',
                 'MONTENEGRO',
                 'MOROCCO',
                 'MOZAMBIQUE',
                 'NAMIBIA',
                 'NEPAL',
                 'NEWZEALAND',
                 'NICARAGUA',
                 'NIGER',
                 'NIGERIA',
                 'NORTHMACEDONIA',
                 'OMAN',
                 'PANAMA',
                 'PAPUANEWGUINEA',
                 'PARAGUAY',
                 'PHILIPPINES',
                 'POLAND',
                 'PORTUGAL',
                 'QATAR',
                 'ROMANIA',
                 'RWANDA',
                 'SAINTKITTSANDNEVIS',
                 'SAINTLUCIA',
                 'SAINTVINCENTANDTHEGRENADINES',
                 'SANMARINO',
                 'SAOTOMEANDPRINCIPE',
                 'SAUDIARABIA',
                 'SENEGAL',
                 'SERBIA',
                 'SEYCHELLES',
                 'SIERRALEONE',
                 'SINGAPORE',
                 'SLOVAKIA',
                 'SLOVENIA',
                 'SOMALIA',
                 'SOUTHAFRICA',
                 'SOUTHSUDAN',
                 'SRILANKA',
                 'SUDAN',
                 'SURINAME',
                 'SYRIA',
                 'TAIWAN',
                 'TAJIKISTAN',
                 'TANZANIA',
                 'THAILAND',
                 'TIMORLESTE',
                 'TOGO',
                 'TRINIDADANDTOBAGO',
                 'TUNISIA',
                 'TURKEY',
                 'UGANDA',
                 'UNITEDARABEMIRATES',
                 'URUGUAY',
                 'UZBEKISTAN',
                 'VENEZUELA',
                 'VIETNAM',
                 'WESTBANKANDGAZA',
                 'WESTERNSAHARA',
                 'YEMEN',
                 'ZAMBIA',
                 'ZIMBABWE']
    countries.sort()
    countries_sheet = gsheets.Sheet(cred_file, scope, sheet_name, 'Countries', state_data)
    countries_sheet.write_data(country_list=countries)


def write_all_data():
    t1 = Thread(target=write_world_data)
    t2 = Thread(target=write_china_data)
    t3 = Thread(target=write_us_data)
    t4 = Thread(target=write_countries_data)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()


def lambda_handler(event, context):
    write_all_data()
    return {
        'statusCode': 200,
        'body': json.dumps('Data logged to Google Sheet!')
    }
