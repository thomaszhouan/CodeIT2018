from flask import Flask
import logging
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.primesum
import codeitsuisse.routes.photogps



