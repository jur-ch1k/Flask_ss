from flask import Blueprint

bluePrint = Blueprint('admin', __name__)

from app.admin import routes
