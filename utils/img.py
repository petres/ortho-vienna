from PIL import Image, ImageDraw

from utils.boxes import rxywh2xywh, xywh2xy_xy

def addOverlayYolo(img, annos, threshold = 0.5):
    # img.putalpha(255)
    draw = ImageDraw.Draw(img, "RGBA")

    # print(len(annos))

    for a in annos:
        # print(a)
        # $mindaro: #cbff8cff;
        # $straw: #e3e36aff;
        # $alloy-orange: #c16200ff;
        # $dark-red: #881600ff;
        # $chocolate-cosmos: #4e0110ff;

        if a['conf'] > threshold:
            draw.rectangle(a['box'], outline="#c16200ff", width=4)
            # draw.rectangle(a['box'], fill=(255, 255, 255, 64))
        else:
            draw.rectangle(a['box'], outline=(255, 255, 255, 128), width=4)
            # draw.rectangle(a['box'], fill=(255, 255, 255, 64))
        
        draw.text((a['box'][2] - 1, a['box'][3]), str(a['conf']), fill=(255, 255, 255, 255), anchor="rd")


    return img