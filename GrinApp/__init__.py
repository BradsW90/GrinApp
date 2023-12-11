"""
The flask application package.
"""

from doctest import debug
from flask import Flask
app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='QWERTY', debug=True)

from . import Login
from . import service
from . import customers
