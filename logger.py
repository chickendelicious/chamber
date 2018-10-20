# Imports the Google Cloud client library
from google.cloud import logging
from google.cloud.logging import DESCENDING


GDOCS_OAUTH_JSON       = '/home/pi/creds/stackdriver_creds.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'chamber_log'


class Logger:
	def __init__(self, name):
		# Instantiates a client
		self.logging_client = logging.Client()
		# The name of the log to write to
		self.log_name = name
		# Selects the log to write to
		self.logger = self.logging_client.logger(self.log_name)
		self.worksheet = None

	def login_open_sheet(self, oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
	    try:
	        scope =  ['https://spreadsheets.google.com/feeds']
	        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
	        gc = gspread.authorize(credentials)
	        worksheet = gc.open(spreadsheet).sheet1
	        return worksheet
	    except Exception as ex:
	        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
	        print('Google sheet login failed with error:', ex)
	        sys.exit(1)



	def log(self, humidity, temp):
		# Writes the log entry
		#self.logger.log_struct(struct)
		if self.worksheet is None:
        	self.worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
        # Append the data in the spreadsheet, including a timestamp
	    try:
	        worksheet.append_row((datetime.datetime.now(), humidity, temp))
	    except:
	        # Error appending data, most likely because credentials are stale.
	        # Null out the worksheet so a login is performed at the top of the loop.
	        print('Append error, logging in again')
	        self.worksheet = None
	        continue

'''
	def list(self):
		FILTER = 'logName:{}'.format(self.log_name)
		return logging_client.list_entries(filter_=FILTER, order_by=DESCENDING)
		''' 
		'''
		for entry in logging_client.list_entries(filter_=FILTER, order_by=DESCENDING):  # API call(s)
			timestamp = entry.timestamp.isoformat()
			print('* {}: {}'.format(timestamp, entry.payload))
		'''
    