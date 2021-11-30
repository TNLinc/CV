from flask import Blueprint

from api.v3.cv.tonal import *

bp = Blueprint("cv_v3", __name__, url_prefix="/api/cv/v3")  # type: Blueprint
