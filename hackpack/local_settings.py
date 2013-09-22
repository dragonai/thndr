'''
Configuration Settings
'''

#Uncomment to configure using the file.  
#WARNING: Be careful not to post your account credentials on GitHub.

TWILIO_ACCOUNT_SID = "AC78084d96f277e973a9f24f1a647a291ca"
TWILIO_AUTH_TOKEN = "82ab425a8dd039b374aaf90cd3bbd200"
TWILIO_APP_SID = "AP79aa540f2331ac32312e6fdcaf3f61b3"
TWILIO_CALLER_ID = "+16789710201"


# Begin Heroku configuration - configured through environment variables.
import os
#TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
#TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', None)
#TWILIO_CALLER_ID = os.environ.get('TWILIO_CALLER_ID', None)
#TWILIO_APP_SID = os.environ.get('TWILIO_APP_SID', None)
