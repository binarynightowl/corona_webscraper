import scripts.sheets as gsheets
import covid19_data

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # use these APIs
cred_file = 'client-secret.json'  # client secret file, do not make this file public!
sheet_name = "COVID-19-CasesOverTime"  # what google sheet to use

state_data = {
}


# get data for any state based on state name and put it in state_data (dict)
def get_state_data(state_to_find):
    state = covid19_data.dataByName(state_to_find)
    state_data[state_to_find] = (state.confirmed - state.deaths - state.recovered)


# get data for all states in a given list and store it to a dictionary
def get_all_state_data():
    states = ["NewYork", "Washington", "NewJersey", "California", "Illinois", "Michigan", "Florida", "Louisiana",
              "Massachusetts", "Texas", "Georgia", "Colorado"]
    for state in states:
        get_state_data(state)


# create a separate sheets instance per workbook, by number
world = gsheets.Sheet(cred_file, scope, sheet_name, 1)
china = gsheets.Sheet(cred_file, scope, sheet_name, 2)
us = gsheets.Sheet(cred_file, scope, sheet_name, 3)

_total = covid19_data.dataByName("Total")
_china = covid19_data.dataByName("China")
_US = covid19_data.dataByName("US")
get_all_state_data()

# write the scraped data to the appropriate Google Sheets
world.write_data(_total.cases, _total.deaths, _total.recovered)
china.write_data(_china.cases, _china.deaths, _china.recovered)
us.write_data(_US.cases, _US.deaths, _US.recovered)
us.write_state_data(state_data)

# cleanup / exit
quit(0)
