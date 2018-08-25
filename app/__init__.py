"""
create by gaowenfeng on 2018/8/25
"""
from flask import Flask

__author__ = "gaowenfeng"


def create_app():
    app = Flask(__name__)
    register_blueprint(app)

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
