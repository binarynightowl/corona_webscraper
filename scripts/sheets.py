import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import strftime
import covid19_data
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime as dtime


class Sheet:

    def __init__(self, credentials, gapi_scope, sheet_name, workbook_name, state_dict=None):
        # create gsheets credentials
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, gapi_scope)
        self.sheet_name = sheet_name

        # create gsheets client
        self.client = gspread.authorize(self.credentials)
        self.state_dict = state_dict

        document = self.client.open(self.sheet_name)
        self.sheet = document.worksheet(workbook_name)
        self.all_data = self.get_all_data()
        self.format_data()
        self.previous_row = self.get_previous_row()

        # Scan for the total number of rows and set the current row to 1 longer
        self.current_line = len(self.all_data) + 1
        self.row_to_write = self.current_line + 1

        self.column_headers = self.sheet.row_values(1)
        self.c_timestamp, self.p_timestamp, self.c_time = self.get_timestamps()

    def get_all_data(self):
        all_data = self.sheet.get_all_records()
        return all_data

    def format_data(self):
        non_decimal = re.compile(r'[^\d.]+')
        for row in self.all_data:
            for key, val in row.items():
                if key != 'Date':
                    if val != '':
                        val = float(non_decimal.sub('', str(val)))
                        row.update({key: val})
                    else:
                        pass

    def get_previous_row(self):
        previous_row = self.all_data[-1]
        return previous_row

    def getColumnIndex(self, name):
        return self.column_headers.index(name) + 1

    def get_timestamps(self):
        current_time = strftime("%Y-%m-%d %H:%M:%S")
        current_timestamp = dtime.timestamp(dtime.strptime(current_time, "%Y-%m-%d %H:%M:%S"))
        previous_timestamp = dtime.timestamp(dtime.strptime(self.previous_row["Date"], "%Y-%m-%d %H:%M:%S"))
        return current_timestamp, previous_timestamp, current_time

    def write_data(self, cases=None, deaths=None, recovered=None, state_data=None, country_list=None):
        headers = self.calculate(cases, deaths, recovered, state_data, country_list)
        location = {}

        for item in headers:
            try:
                location.update({self.getColumnIndex(item): item})
            except ValueError:
                pass

        max_index = range(1, self.sheet.col_count + 1)

        row_to_write = []

        for column in max_index:
            try:
                row_to_write.append(headers[location[column]])
            except KeyError:
                row_to_write.append('')
        self.sheet.append_row(row_to_write, table_range='A1')

    def calculate(self, cases=None, deaths=None, recovered=None, state_data=None, country_list=None):
        if recovered is None:
            recovered = 0

        if cases and deaths is not None:
            active = (cases - deaths) - recovered
        else:
            active = 1
            cases = 1
            deaths = 1
            recovered = 1

        days = (self.c_timestamp - self.p_timestamp) / 86400
        try:
            dDeaths = round((deaths - self.previous_row.get('Deaths')) / days, 0)
            dActive = round((active - self.previous_row.get('Active')) / days, 0)
            dRecovered = round((recovered - self.previous_row.get('Recovered')) / days, 0)
            five_recovered = dRecovered
            five_deaths = dDeaths
            dCases = round((cases - self.previous_row.get('Cases')) / days, 0)
            for item in self.all_data[-4:]:
                deltaR = item.get('dRecovered')
                deltaD = item.get('dDeaths')
                if deltaD is None or deltaR is None:
                    five_deaths = 1
                    five_recovered = 0
                else:
                    five_recovered += float(deltaR)
                    five_deaths += float(deltaD)
        except TypeError:
            dDeaths, dActive, dRecovered, five_recovered, dCases = 0, 0, 0, 0, 0
            five_deaths = 1
        except ValueError:
            dDeaths, dActive, dRecovered, five_recovered, dCases = 0, 0, 0, 0, 0
            five_deaths = 1

        headers = {
            "Date": self.c_time,
            "Cases": cases,
            "Deaths": deaths,
            "Recovered": recovered,
            "Active": active,
            "pDeaths": deaths / cases,
            "pRecovered": recovered / cases,
            "pActive": active / cases,
            "R/D": recovered / deaths,
            "Days": days,
            "dCases": dCases,
            "dDeaths": dDeaths,
            "dActive": dActive,
            "dRecovered": dRecovered,
            "5 day heal:death": five_recovered / five_deaths
        }

        sum51 = 0
        if state_data is not None:
            for state in self.state_dict:
                headers.update({state: state_data[state]})
                sum51 += state_data[state]
            headers.update({"51 Sum": sum51, "51 Sum Diff": abs(cases - sum51), "p51 Diff": (1 - (sum51 / cases))})
        else:
            pass

        if country_list is not None:
            for country in country_list:
                data = covid19_data.dataByName(country)
                headers.update({country: data.confirmed})
        else:
            pass

        self.all_data.append(headers)
        return headers
