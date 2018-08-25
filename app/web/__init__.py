"""
create by gaowenfeng on 2018/8/25
"""
from flask import Blueprint

__author__ = "gaowenfeng"

web = Blueprint('web', __name__)

from app.web import communication
