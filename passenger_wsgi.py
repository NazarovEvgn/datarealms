import os, sys
sys.path.insert(0, '/home/e/evgenyca/datarealms.ru/Datarealms')
sys.path.insert(1, '/home/e/evgenyca/datarealms.ru/venv_django/lib/python3.13/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Datarealms.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()