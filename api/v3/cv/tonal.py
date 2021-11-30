import http
from typing import Optional

import numpy as np
from cv2 import cv2
from flask_apispec import doc
from flask_apispec import marshal_with
from flask_apispec import use_kwargs
from marshmallow import fields
from marshmallow import validate
from werkzeug.datastructures import FileStorage

from api.v3.cv import bp
from schemas.color_schema import ColorSchema
from schemas.error_schema import ErrorSchema
from schemas.input_image_schema import InputImageSchema
from services.cv_tone_processor import CVToneProcessor
from services.face_extractor import face_extractor_fabric
from services.tone_extractor import tone_extractor_fabric
from services.white_balance import white_balance_fabric


@bp.route("/skin_tone", methods=["POST"])
@doc(
    description="Search face on the photo and determine its skin color",
    tags=["tonal"],
    consumes=["multipart/form-data"],
)
@use_kwargs(InputImageSchema, location="files")
@use_kwargs(
    {
        "wb":
        fields.String(default=None,
                      validate=validate.OneOf(white_balance_fabric.keys()))
    },
    location="query",
)
@use_kwargs(
    {
        "face_ext":
        fields.String(default="mediapipe",
                      validate=validate.OneOf(face_extractor_fabric.keys()))
    },
    location="query",
)
@use_kwargs(
    {
        "tone_ext":
        fields.String(default="kmean",
                      validate=validate.OneOf(tone_extractor_fabric.keys()))
    },
    location="query",
)
@marshal_with(schema=ColorSchema,
              code=200,
              description="Return color in hex code")
@marshal_with(schema=ErrorSchema,
              code=422,
              description="Problem with image file")
@marshal_with(schema=ErrorSchema, code=400, description="No face on the image")
def skin_tone_v3(
    image: FileStorage,
    face_ext: str = "mediapipe",
    tone_ext: str = "kmean",
    wb: Optional[str] = None,
):
    np_img = np.fromstring(image.read(), np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    color = CVToneProcessor.build_tone_process(image, face_ext, tone_ext, wb)

    if not color:
        error = {"files": {"image": ["No face on the image"]}}
        return ErrorSchema().dump({"error":
                                   error}), http.HTTPStatus.BAD_REQUEST

    response = dict(color=color)
    return ColorSchema().dump(response)
