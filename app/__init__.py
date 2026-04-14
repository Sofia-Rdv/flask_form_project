from flask import Flask
import logging
from logging_module.my_logger_config import setup_logging

app = Flask(__name__)
from app import routes
setup_logging()