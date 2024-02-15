import os, sys, json

from flask import Flask, Blueprint, jsonify

from .bp.img import bp as img_bp
from .bp.inf import bp as inf_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.json", load=json.load)

    base = Blueprint('dashboard', __name__)
    base.register_blueprint(img_bp, url_prefix='/img')
    base.register_blueprint(inf_bp, url_prefix='/inf')

    app.register_blueprint(base, url_prefix='/')
    
    return app
