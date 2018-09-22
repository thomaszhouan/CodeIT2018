from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.primesum
import codeitsuisse.routes.tally_expenses

