from api.v3.cv.tonal import *
from flask import Blueprint

bp = Blueprint("cv_v3", __name__, url_prefix="/api/cv/v3")  # type: Blueprint
