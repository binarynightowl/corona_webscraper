import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import strftime
from threading import Thread


class Sheet:

    def __init__(self, credentials, gapi_scope, sheet_name, workbook_num, state_dict=None):
        # create gsheets credentials
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, gapi_scope)
        self.sheet_name = sheet_name
        self.workbook_num = workbook_num - 1
        # create gsheets client
        self.client = gspread.authorize(self.credentials)
        self.state_dict = state_dict

        document = self.client.open(self.sheet_name)
        self.sheet = document.get_worksheet(self.workbook_num)

        # Scan for the total number of rows and set the current row to 1 longer
        self.current_line = self.sheet.row_count
        self.row_to_write = self.current_line + 1
        self.previous_row = self.current_line

        self.column_headers = self.sheet.row_values(1)

    def getColumnIndex(self, name):
        return self.column_headers.index(name) + 1

    def write_data(self, cases, deaths, recovered, state_data=None):
        active = (cases - deaths) - recovered
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

        headers.update({"51 Sum": sum51})
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
