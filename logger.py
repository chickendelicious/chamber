# Imports the Google Cloud client library
from google.cloud import logging
from google.cloud.logging import DESCENDING


class Logger:
	def __init__(self, name):
		# Instantiates a client
		self.logging_client = logging.Client()
		# The name of the log to write to
		self.log_name = name
		# Selects the log to write to
		self.logger = self.logging_client.logger(self.log_name)

	def log(self, struct):
		# Writes the log entry
		self.logger.log_struct(struct)

	def list(self):
		FILTER = 'logName:{}'.format(self.log_name)
		return logging_client.list_entries(filter_=FILTER, order_by=DESCENDING)
		'''
		for entry in logging_client.list_entries(filter_=FILTER, order_by=DESCENDING):  # API call(s)
			timestamp = entry.timestamp.isoformat()
			print('* {}: {}'.format(timestamp, entry.payload))
		'''
        