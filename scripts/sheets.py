import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime


class Sheet:

    def __init__(self, credentials, gapi_scope, sheet_name, workbook_num):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, gapi_scope)
        self.sheet_name = sheet_name
        self.workbok_num = workbook_num - 1
        self.client = gspread.authorize(self.credentials)

        document = self.client.open("COVID-19-CasesOverTime")
        self.sheet = document.get_worksheet(self.workbok_num)

        self.get_old_data()

    def get_old_data(self):
        # Scan for the total number of rows and set the current row to 1 longer
        self.current_line = self.sheet.row_count
        self.old_cases = self.sheet.cell(self.current_line, 2).value
        self.old_deaths = self.sheet.cell(self.current_line, 3).value
        self.old_recovered = self.sheet.cell(self.current_line, 4).value
        self.old_active = self.sheet.cell(self.current_line, 5).value
        self.old_deaths_per = self.sheet.cell(self.current_line, 7).value
        self.old_recovered_per = self.sheet.cell(self.current_line, 8).value
        self.old_active_per = self.sheet.cell(self.current_line, 9).value

    def write_data(self, cases, deaths, recovered):
        active = (cases - deaths) - recovered
        self.row_to_write = self.current_line + 1  # crappy code fix this later
        current_time = datetime.datetime.now()
        self.sheet.resize(self.row_to_write)
        self.sheet.update_cell(self.row_to_write, 1,  # crappy code fix this later
                               "{}-{}-{}".format(current_time.year, current_time.month, current_time.day))
        self.sheet.update_cell(self.row_to_write, 2, cases)
        self.sheet.update_cell(self.row_to_write, 3, deaths)
        self.sheet.update_cell(self.row_to_write, 4, recovered)
        self.sheet.update_cell(self.row_to_write, 5, active)
        self.sheet.update_cell(self.row_to_write, 7, deaths / cases)
        self.sheet.update_cell(self.row_to_write, 8, recovered / cases)
        self.sheet.update_cell(self.row_to_write, 9, active / cases)

    def write_state_data(self, state_data):
        ny, wa, nj, ca, il, mi, fl, la, ma, tx, ga, co = state_data  # crappy code fix this later
        self.sheet.update_cell(self.row_to_write, 13, ny)
        self.sheet.update_cell(self.row_to_write, 14, wa)
        self.sheet.update_cell(self.row_to_write, 15, nj)
        self.sheet.update_cell(self.row_to_write, 16, ca)
        self.sheet.update_cell(self.row_to_write, 17, il)
        self.sheet.update_cell(self.row_to_write, 18, mi)
        self.sheet.update_cell(self.row_to_write, 19, fl)
        self.sheet.update_cell(self.row_to_write, 20, la)
        self.sheet.update_cell(self.row_to_write, 21, ma)
        self.sheet.update_cell(self.row_to_write, 22, tx)
        self.sheet.update_cell(self.row_to_write, 23, ga)
        self.sheet.update_cell(self.row_to_write, 24, co)
