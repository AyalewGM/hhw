import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/hhw/")

# Load environment variables from .env file
env_file = '/var/www/hhw/.env'
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from nutras import app as application
application.secret_key = os.environ.get('SECRET_KEY', 'HEREISMYSECRET121')
