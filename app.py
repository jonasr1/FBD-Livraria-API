# Connect to your postgres DB
from datetime import datetime, timedelta
import random

import psycopg2
# from faker import Faker
from flask import Flask, jsonify, Response, make_response, request

from modules.cliente.controller import cliente_controller
# from modules.marca.controller import marca_controller
# from modules.produto.controller import produto_controller
from service.connect import Connect

app = Flask(__name__)
app.register_blueprint(cliente_controller)
# app.register_blueprint(categoria_controller)
# app.register_blueprint(produto_controller)
Connect().create_tables()
app.run(debug=True)