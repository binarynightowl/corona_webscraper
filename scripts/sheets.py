import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import strftime
import covid19_data


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

        # Scan for the total number of rows and set the current row to 1 longer
        self.current_line = self.sheet.row_count
        self.row_to_write = self.current_line + 1
        self.previous_row = self.current_line

        self.column_headers = self.sheet.row_values(1)

    def getColumnIndex(self, name):
        return self.column_headers.index(name) + 1

    def write_data(self, cases=None, deaths=None, recovered=None, state_data=None, country_list=None):
        if cases and deaths and recovered is not None:
            active = (cases - deaths) - recovered
        else:
            active = 1
            cases = 1
            deaths = 1
            recovered = 1
        current_time = strftime("%Y-%m-%d %H:%M:%S")

        headers = {
            "Date": current_time,
            "Cases": cases,
            "Deaths": deaths,
            "Recovered": recovered,
            "Active": active,
            "pDeaths": deaths / cases,
            "pRecovered": recovered / cases,
            "pActive": active / cases,
            "R/D": recovered / deaths,
        }
        sum51 = 0
        if state_data is not None:
            for state in self.state_dict:
                headers.update({state: state_data[state]})
                sum51 += state_data[state]
        else:
            pass

        if country_list is not None:
            for country in country_list:
                data = covid19_data.dataByName(country)
                headers.update({country: data.confirmed})
        else:
            pass

        headers.update({"51 Sum": sum51})
        if sum51 != 0:
            headers.update({"51 Sum Diff": cases - sum51})
            headers.update({"p51 Diff": (((cases / sum51) - (sum51 / cases)) / 2)})
        else:
            pass
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
