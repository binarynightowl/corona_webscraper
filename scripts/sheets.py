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

        self.get_old_data()
        self.column_headers = self.sheet.row_values(1)
        print(self.column_headers)

    def get_old_data(self):  # not currently  used - will be implemented later
        self.old_cases = self.sheet.cell(self.current_line, 2).value
        self.old_deaths = self.sheet.cell(self.current_line, 3).value
        self.old_recovered = self.sheet.cell(self.current_line, 4).value
        self.old_active = self.sheet.cell(self.current_line, 5).value
        self.old_deaths_per = self.sheet.cell(self.current_line, 7).value
        self.old_recovered_per = self.sheet.cell(self.current_line, 8).value
        self.old_active_per = self.sheet.cell(self.current_line, 9).value

    def write_data(self, cases, deaths, recovered):
        active = (cases - deaths) - recovered
        current_time = strftime("%Y-%m-%d %H:%M:%S")
        self.sheet.resize(self.row_to_write)
        self.sheet.update_cell(self.row_to_write, 1, current_time)
        self.sheet.update_cell(self.row_to_write, 2, cases)  # row, column, data to write to cell
        self.sheet.update_cell(self.row_to_write, 3, deaths)
        self.sheet.update_cell(self.row_to_write, 4, recovered)
        self.sheet.update_cell(self.row_to_write, 5, active)
        self.sheet.update_cell(self.row_to_write, 7, deaths / cases)
        self.sheet.update_cell(self.row_to_write, 8, recovered / cases)
        self.sheet.update_cell(self.row_to_write, 9, active / cases)

    def write_state_data(self, state_data):
        for state in self.state_dict:
            self.sheet.update_cell(self.row_to_write, self.column_headers.index(state) + 1, state_data[state])
