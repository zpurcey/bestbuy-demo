#!/usr/bin/python

import sys
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/var/www/")
sys.path.insert(0,"/var/www/backend")

from backend import app as application
