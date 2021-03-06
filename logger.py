from oauth2client.service_account import ServiceAccountCredentials
import gspread, datetime

GDOCS_OAUTH_JSON	   = '/home/pi/creds/stackdriver_creds.json'
GDOCS_SPREADSHEET_NAME = 'chamber_log2'
ERROR_SHEET = 'chamber_errors'

class Logger:
	def __init__(self, name):
		#self.logging_client = logging.Client()
		self.log_name = name
		#self.logger = self.logging_client.logger(self.log_name)
		self.worksheet = None
		self.errorsheet = None

	def login_open_sheet(self, oauth_key_file, spreadsheet):
		try:
			scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
			credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
			gc = gspread.authorize(credentials)
			worksheet = gc.open(spreadsheet).sheet1
			return worksheet
		except Exception as ex:
			print('Google sheet login failed with error:', ex)

	def log(self, humidity, temp):
		if self.worksheet is None:
			self.worksheet = self.login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
		try:
			time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%z')
			self.worksheet.append_row((time, humidity, temp))
		except Exception as ex:
			print('Append error: ', ex)
			self.worksheet = None

	def log_error(self, error, data=None):
		if self.errorsheet is None:
			self.errorsheet = self.login_open_sheet(GDOCS_OAUTH_JSON, ERROR_SHEET)
		try:
			time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%z')
			self.errorsheet.append_row((time, error, data))
		except Exception as ex:
			print('Append error: ', ex)
			self.errorsheet = None

	