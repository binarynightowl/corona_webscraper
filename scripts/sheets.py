import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt

date_time = dt.datetime


class Sheet:

    def __init__(self, credentials, gapi_scope, sheet_name, workbook_num):
        # create gsheets credentials
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, gapi_scope)
        self.sheet_name = sheet_name
        self.workbook_num = workbook_num - 1
        # create gsheets client
        self.client = gspread.authorize(self.credentials)

        document = self.client.open(self.sheet_name)
        self.sheet = document.get_worksheet(self.workbook_num)

        # Scan for the total number of rows and set the current row to 1 longer
        self.current_line = self.sheet.row_count
        self.row_to_write = self.current_line + 1

        self.get_old_data()

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
        current_time = date_time.now()
        current_time = "{}-{}-{} @ {}:{}".format(current_time.year, current_time.month, current_time.day,
                                                 current_time.hour,
                                                 current_time.minute)
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
        self.sheet.update_cell(self.row_to_write, 13, state_data['Alaska'])
        self.sheet.update_cell(self.row_to_write, 14, state_data['Alabama'])
        self.sheet.update_cell(self.row_to_write, 15, state_data['Arkansas'])
        self.sheet.update_cell(self.row_to_write, 16, state_data['Arizona'])
        self.sheet.update_cell(self.row_to_write, 17, state_data['California'])
        self.sheet.update_cell(self.row_to_write, 18, state_data['Colorado'])
        self.sheet.update_cell(self.row_to_write, 19, state_data['Connecticut'])
        self.sheet.update_cell(self.row_to_write, 20, state_data['District of Columbia'])
        self.sheet.update_cell(self.row_to_write, 21, state_data['Delaware'])
        self.sheet.update_cell(self.row_to_write, 22, state_data['Florida'])
        self.sheet.update_cell(self.row_to_write, 23, state_data['Georgia'])
        self.sheet.update_cell(self.row_to_write, 24, state_data['Hawaii'])
        self.sheet.update_cell(self.row_to_write, 25, state_data['Iowa'])
        self.sheet.update_cell(self.row_to_write, 26, state_data['Idaho'])
        self.sheet.update_cell(self.row_to_write, 27, state_data['Illinois'])
        self.sheet.update_cell(self.row_to_write, 28, state_data['Indiana'])
        self.sheet.update_cell(self.row_to_write, 29, state_data['Kansas'])
        self.sheet.update_cell(self.row_to_write, 30, state_data['Kentucky'])
        self.sheet.update_cell(self.row_to_write, 31, state_data['Louisiana'])
        self.sheet.update_cell(self.row_to_write, 32, state_data['Massachusetts'])
        self.sheet.update_cell(self.row_to_write, 33, state_data['Maryland'])
        self.sheet.update_cell(self.row_to_write, 34, state_data['Maine'])
        self.sheet.update_cell(self.row_to_write, 35, state_data['Michigan'])
        self.sheet.update_cell(self.row_to_write, 36, state_data['Minnesota'])
        self.sheet.update_cell(self.row_to_write, 37, state_data['Missouri'])
        self.sheet.update_cell(self.row_to_write, 38, state_data['Mississippi'])
        self.sheet.update_cell(self.row_to_write, 39, state_data['Montana'])
        self.sheet.update_cell(self.row_to_write, 40, state_data['North Carolina'])
        self.sheet.update_cell(self.row_to_write, 41, state_data['North Dakota'])
        self.sheet.update_cell(self.row_to_write, 42, state_data['Nebraska'])
        self.sheet.update_cell(self.row_to_write, 43, state_data['New Hampshire'])
        self.sheet.update_cell(self.row_to_write, 44, state_data['New Jersey'])
        self.sheet.update_cell(self.row_to_write, 45, state_data['New Mexico'])
        self.sheet.update_cell(self.row_to_write, 46, state_data['Nevada'])
        self.sheet.update_cell(self.row_to_write, 47, state_data['New York'])
        self.sheet.update_cell(self.row_to_write, 48, state_data['Ohio'])
        self.sheet.update_cell(self.row_to_write, 49, state_data['Oklahoma'])
        self.sheet.update_cell(self.row_to_write, 50, state_data['Oregon'])
        self.sheet.update_cell(self.row_to_write, 51, state_data['Pennsylvania'])
        self.sheet.update_cell(self.row_to_write, 52, state_data['Rhode Island'])
        self.sheet.update_cell(self.row_to_write, 53, state_data['South Carolina'])
        self.sheet.update_cell(self.row_to_write, 54, state_data['South Dakota'])
        self.sheet.update_cell(self.row_to_write, 55, state_data['Tennessee'])
        self.sheet.update_cell(self.row_to_write, 56, state_data['Texas'])
        self.sheet.update_cell(self.row_to_write, 57, state_data['Utah'])
        self.sheet.update_cell(self.row_to_write, 58, state_data['Virginia'])
        self.sheet.update_cell(self.row_to_write, 59, state_data['Vermont'])
        self.sheet.update_cell(self.row_to_write, 60, state_data['Washington'])
        self.sheet.update_cell(self.row_to_write, 61, state_data['Wisconsin'])
        self.sheet.update_cell(self.row_to_write, 62, state_data['West Virginia'])
        self.sheet.update_cell(self.row_to_write, 63, state_data['Wyoming'])
