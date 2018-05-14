from flask import Blueprint


bp = Blueprint('model', __name__)

from app.model import routes
