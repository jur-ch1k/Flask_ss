from flask import Blueprint

bluePrint = Blueprint('teacher', __name__)

from app.teacher import routes
