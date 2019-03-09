import os
import sys

import django

PROJDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJDIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodbank.settings")

django.setup()
