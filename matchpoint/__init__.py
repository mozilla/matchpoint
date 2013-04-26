from __future__ import absolute_import
import logging

from flask import Flask


app = Flask(__name__)


log_handler = logging.StreamHandler()
log_handler.setLevel(logging.WARNING)
app.logger.addHandler(log_handler)


import matchpoint.views
