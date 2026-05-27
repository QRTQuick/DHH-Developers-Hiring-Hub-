import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DJANGO_DIR = BASE_DIR / 'DHH'

if str(DJANGO_DIR) not in sys.path:
    sys.path.insert(0, str(DJANGO_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DHH.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
