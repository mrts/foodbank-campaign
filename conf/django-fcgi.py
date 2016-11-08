import sys, os

APPNAME = "toidupank"

APPDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_BIN_DIR = APPDIR + "/venv/bin"

# Setup virtualenv
os.environ.setdefault('PATH', '/sbin:/bin:/usr/sbin:/usr/bin')
os.environ['PATH'] = VENV_BIN_DIR + ':' + os.environ['PATH']
os.environ['VIRTUAL_ENV'] =  VENV_BIN_DIR
os.environ['PYTHON_EGG_CACHE'] = VENV_BIN_DIR

# Add site to Python path.
sys.path.insert(0, os.path.join(APPDIR, 'src'))

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % APPNAME

from django_fastcgi.servers.fastcgi import runfastcgi
from django.core.servers.basehttp import get_internal_wsgi_application

wsgi_application = get_internal_wsgi_application()
runfastcgi(wsgi_application, method="threaded", daemonize="false")
