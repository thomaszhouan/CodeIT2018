from flask import Flask
import logging
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.primesum
import codeitsuisse.routes.photogps
import codeitsuisse.routes.tally_expenses
# import codeitsuisse.routes.deep_learning
import codeitsuisse.routes.broadcaster
import codeitsuisse.routes.airTrafficController
import codeitsuisse.routes.broadcaster_q1
import codeitsuisse.routes.skilltree
import codeitsuisse.routes.hotel
import codeitsuisse.routes.twodinosaurs
