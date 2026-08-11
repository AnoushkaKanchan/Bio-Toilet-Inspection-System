import os

if os.getenv("DJANGO_ENV", "development").lower() == "production":
    from .production import *
else:
    from .development import *