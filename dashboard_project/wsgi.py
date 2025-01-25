import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_project.settings')

application = get_wsgi_application()

# Add static files serving configuration
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(application)