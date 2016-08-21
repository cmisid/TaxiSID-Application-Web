import sys, os, logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/taxisid')
os.chdir('/var/www/taxisid')
from run import app
application = app