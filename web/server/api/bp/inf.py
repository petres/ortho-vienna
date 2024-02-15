import sys, os, io

from flask import jsonify, request, Blueprint, send_file, Response
from ultralytics import YOLO

from pathlib import Path
from PIL import Image, ImageDraw

prj_dir = Path(os.path.dirname(__file__))
while ".git" not in os.listdir(prj_dir): prj_dir /= ".."
sys.path.append(str(prj_dir.resolve()))

from utils.coords import getImgFor
from utils.img import addOverlayYolo

bp = Blueprint('inf', __name__)


print(list(Path(prj_dir/'data/model').glob("*.pt")))

models = {m.stem: {
    'file': m,
    'model': YOLO(m)
} for m in (prj_dir/'data/model').iterdir()}

# print(models)

@bp.route('/models', methods=['GET'])
def getModels():
    return jsonify({
        'valid': True,
        'models': list(models.keys()),
    })


def getInference(img, model_name):
    results = models[model_name]['model']([img])
    return results[0]


@bp.route('/annotation_json/<model>/<layer>/<float:lng1>/<float:lat1>/<float:lng2>/<float:lat2>/<int:zoom>', methods=['GET'])
def annotation_json(model, layer, lng1, lat1, lng2, lat2, zoom):
    img = getImgFor([lng1, lat1, lng2, lat2], zoom, layer = layer)

    result = getInference(img, model)

    info = [{
        'cls': round(e.cls[0].item()),
        'conf': round(e.conf[0].item(), 2),
        'box': [round(c) for c in e.xyxy.tolist()[0]],

    } for e in result.boxes]
    
    return jsonify(info)



@bp.route('/annotation_txt/<model>/<layer>/<float:lng1>/<float:lat1>/<float:lng2>/<float:lat2>/<int:zoom>', methods=['GET'])
def annotation_txt(model, layer, lng1, lat1, lng2, lat2, zoom):
    img = getImgFor([lng1, lat1, lng2, lat2], zoom, layer = layer)

    result = getInference(img, model)
    result.save_txt('ttt.txt', save_conf=False)

    with open('ttt.txt', 'r') as f:
        return Response(f.read(), mimetype='text/plain')


@bp.route('/img-annotated-yolo/<model>/<layer>/<float:lng1>/<float:lat1>/<float:lng2>/<float:lat2>/<int:zoom>', methods=['GET'])
def annotatedYolo(model, layer, lng1, lat1, lng2, lat2, zoom):
    img = getImgFor([lng1, lat1, lng2, lat2], zoom, layer = layer)

    result = getInference(img, model)
    a = result.plot()
    
    imgAnno = Image.fromarray(a[:, :, ::-1])

    bs = io.BytesIO()
    imgAnno.save(bs, format="PNG")
    bs.seek(0)

    return send_file(
        bs,
        mimetype='image/png'
    )

@bp.route('/img-annotated-self/<model>/<layer>/<float:lng1>/<float:lat1>/<float:lng2>/<float:lat2>/<int:zoom>', methods=['GET'])
def annotatedSelf(model, layer, lng1, lat1, lng2, lat2, zoom):
    img = getImgFor([lng1, lat1, lng2, lat2], zoom, layer = layer)

    result = getInference(img, model)

    img = addOverlayYolo(img, [{
        'cls': round(e.cls[0].item()),
        'conf': round(e.conf[0].item(), 2),
        'box': [round(c) for c in e.xyxy.tolist()[0]],
    } for e in result.boxes])

    bs = io.BytesIO()
    img.save(bs, format="PNG")
    bs.seek(0)

    return send_file(
        bs,
        mimetype='image/png'
    )
