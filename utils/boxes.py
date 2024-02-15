def xxyy2rxywh(box, size):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x, y, w, h = x*dw, y*dh, w*dw, h*dh
    return (x, y, w, h)

def xywh2xy_xy(bbox):
    return ((bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]))

def xyxy2xywh(bbox):
    return (bbox[0], bbox[1], (bbox[2] - bbox[0]), (bbox[3] - bbox[1]))

def xywh2xxyy(bbox):
    return (bbox[0], bbox[0] + bbox[2], bbox[1], bbox[1] + bbox[3])

def xywh2rxywh(bbox, size):
    return xxyy2rxywh(xywh2xxyy(bbox), size)


def rxywh2xywh(box, size, r = True):
    w = box[2]
    h = box[3]
    x = box[0] - w/2.0
    y = box[1] - h/2.0
    x, y, w, h = x*size[0], y*size[1], w*size[0], h*size[1]
    if r:
        x, y, w, h = round(x), round(y), round(w), round(h)
    return (x, y, w, h)


def rxyxy2xywh(box, size, r = True):
    x = box[0] 
    y = box[1] 

    w = box[2] - box[0] 
    h = box[3] - box[1] 

    x, y, w, h = x*size[0], y*size[1], w*size[0], h*size[1]
    if r:
        x, y, w, h = round(x), round(y), round(w), round(h)
    return (x, y, w, h)

