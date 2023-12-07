#!/usr/bin/env python3
"""Flask App Config"""

import pathlib

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

def create_app():
    """Create Flask app"""
    this_app = Flask(__name__)
    this_app.secret_key = 'secret'
    if not pathlib.Path(".flaskenv").exists():
        load_dotenv(pathlib.Path(__file__).parent / pathlib.Path(".flaskenv"))
    this_app.config.from_prefixed_env()
    return this_app

app = create_app()

this_dir = pathlib.Path(__file__).parent
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
    this_dir / pathlib.Path("banking.sqlite3")
)

db = SQLAlchemy(app)

ma = Marshmallow(app)