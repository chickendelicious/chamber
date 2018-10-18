from google.cloud import logging
from google.cloud.logging import DESCENDING

logging_client = logging.Client()
# The name of the log to write to
log_name = 'chamber'
# Selects the log to write to
logger = logging_client.logger(log_name)
FILTER = 'logName:{}'.format(log_name)
for entry in logging_client.list_entries(filter_=FILTER, order_by=DESCENDING):  # API call(s)
    timestamp = entry.timestamp.isoformat()
    print('* {}: {}'.format(timestamp, entry.payload))
		