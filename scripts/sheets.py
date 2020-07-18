import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import strftime


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

    def write_state_data(self, state_data):
        for state in self.state_dict:
            self.sheet.update_cell(self.row_to_write, self.column_headers.index(state) + 1, state_data[state])

    def write_data(self, cases, deaths, recovered):
        active = (cases - deaths) - recovered
        current_time = strftime("%Y-%m-%d %H:%M:%S")

        self.sheet.resize(self.row_to_write)
        headers = {
            "Date": current_time,
            "Cases": cases,
            "Deaths": deaths,
            "Recovered": recovered,
            "Active": active,
            "pDeaths": deaths / cases,
            "pRecovered": recovered / cases,
            "pActive": active / cases,
            "R/D": recovered / deaths
        }

        for item in headers:
            self.sheet.update_cell(self.row_to_write, self.getColumnIndex(item), str(headers[item]))
