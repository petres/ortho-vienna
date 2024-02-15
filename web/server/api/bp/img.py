import sys, os, io

from flask import jsonify, request, Blueprint, send_file

from pathlib import Path
from PIL import Image, ImageDraw

prj_dir = Path(os.path.dirname(__file__))
while ".git" not in os.listdir(prj_dir): prj_dir /= ".."
sys.path.append(str(prj_dir.resolve()))

from utils.coords import *

bp = Blueprint('img', __name__)


img_formats = {
    'PNG': 'png',
    'JPEG': 'jpg'
}

@bp.route('/<layer>/<float:lng1>/<float:lat1>/<float:lng2>/<float:lat2>/<int:zoom>/<format>', methods=['GET'])
def get(layer, lng1, lat1, lng2, lat2, zoom, format):
    img =  getImgFor([lng1, lat1, lng2, lat2], zoom, layer = layer)
  
    bs = io.BytesIO()
    img.save(bs, format=format)
    bs.seek(0)

    return send_file(
        bs,
        mimetype=f'image/{img_formats[format]}'
    )

