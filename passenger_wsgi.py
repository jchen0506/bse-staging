import sys
import os

INTERP = os.path.join(os.environ['HOME'], 'bse_website', 'venv', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())
sys.path.append('bse_website')


# create the production app for wsgi
os.environ['FLASK_CONFIG'] = 'production'
from bse_website import app as application
