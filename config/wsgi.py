import os

import pymysql
pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

app = application

