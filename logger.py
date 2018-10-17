# Imports the Google Cloud client library
from google.cloud import logging


# Instantiates a client
logging_client = logging.Client()

# The name of the log to write to
log_name = 'chamber'
# Selects the log to write to
logger = logging_client.logger(log_name)

# The data to log
struct = {'Humidity': 0, 'Temp': 0}

# Writes the log entry
logger.log_struct(struct)

print('Logged: {}'.format(text))