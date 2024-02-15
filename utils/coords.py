from owslib.wmts import WebMapTileService
import mercantile
from PIL import Image
from io import BytesIO
import math

url = 'https://mapsneu.wien.gv.at/wmtsneu/1.0.0/WMTSCapabilities.xml'
wmts = WebMapTileService(url)

bboxes_4326 = {
    'vienna': (16.083   , 48       , 16.704   , 48.4),
    'obdo':   (16.366995, 48.223275, 16.372644, 48.226384),
    'gauss':  (16.3688, 48.2256, 16.371, 48.2269),
}


bboxes_3857 = {
    'vienna': (1799977.3606, 6125395.9172, 1847482.9737, 6161779.9426),
    'obdo':   (1821965.5467, 6144080.5904, 1822594.3606, 6144600.1234),
    'gauss':  (1822166, 6144469, 1822411, 6144686),
}

def getTile(tile_coord, wmts = wmts, layer = "lb"):
    x, y, z = tile_coord
    return  wmts.gettile(
        layer=layer,
        tilematrix=z,
        row=y,
        column=x
    )
    
def getTileImg(tile_coord, wmts = wmts, layer = "lb"):
    return Image.open(BytesIO(getTile(tile_coord, wmts, layer).read()))


def getTilesForBBox(bbox, zoom, epsg = 4326):
    west, south, east, north = bbox

    if epsg == 3857:
        west, south = mercantile.lnglat(west, south)
        east, north = mercantile.lnglat(east, north)

    # print((west, south, east, north))

    return [(tile.x, tile.y, tile.z) for tile in mercantile.tiles(west, south, east, north, zooms=zoom)]


# def getImgFor(bbox, zoom, wmts, layer, epsg = 4326):
#     tile_size = 256

#     tiles_img = {}
#     for tc in getTilesForBBox(bbox, zoom, epsg):
#         tiles_img[tc] = getTileImg(tc, wmts, layer)

#     if len(tiles_img) == 0:
#         return None
    
#     x_vals = [k[0] for k in tiles_img.keys()]
#     x_min, x_max = min(x_vals), max(x_vals)

#     y_vals = [k[1] for k in tiles_img.keys()]
#     y_min, y_max = min(y_vals), max(y_vals)

#     ws = mercantile.ul(x_min, y_min, zoom)
#     en = mercantile.ul(x_max + 1, y_max + 1, zoom)

#     west, south = mercantile.lnglat(ws)
#     east, north = mercantile.lnglat(en)

#     print(west, south)
#     print(east, north)

#     img = Image.new('RGB', (256*(x_max-x_min+1), 256*(y_max-y_min+1)), "white")

#     for tc, i in tiles_img.items():
#         img.paste(i, ((tc[0] - x_min)*tile_size, (tc[1] - y_min)*tile_size))

#     return img





def getImgFor(bbox, zoom, wmts = wmts, layer = "lb", epsg = 4326):
    tile_size = 256

    tiles_img = {}
    tiles = getTilesForBBox(bbox, zoom, epsg)
    if len(tiles) > 256:
        raise Exception('TOO MUCH TILES')

    if len(tiles) == 0:
        raise Exception('NO TILES')

    for tc in tiles:
        tiles_img[tc] = getTileImg(tc, wmts, layer)

    x_vals = [k[0] for k in tiles_img.keys()]
    x_min, x_max = min(x_vals), max(x_vals)

    y_vals = [k[1] for k in tiles_img.keys()]
    y_min, y_max = min(y_vals), max(y_vals)

    ws = mercantile.ul(x_min, y_min, zoom)
    en = mercantile.ul(x_max + 1, y_max + 1, zoom)

    west, south = mercantile.xy(ws.lng, ws.lat)
    east, north = mercantile.xy(en.lng, en.lat)

    bbox_tiles = (west, south, east, north)

    img = Image.new('RGB', (256*(x_max-x_min+1), 256*(y_max-y_min+1)), "white")

    for tc, i in tiles_img.items():
        img.paste(i, ((tc[0] - x_min)*tile_size, (tc[1] - y_min)*tile_size))

    # print('requested: ', bbox)
    # print('      got: ', bbox_tiles)

    def toImgCoords(coord):
        x_0, x_1 = bbox_tiles[0], bbox_tiles[2]
        y_0, y_1 = bbox_tiles[3], bbox_tiles[1]
        return (
            round((coord[0] - x_0)/(x_1 - x_0)*img.size[0]),
            round((1 - (coord[1] - y_0)/(y_1 - y_0))*img.size[1]),
        )

    if epsg == 4326:
        p1 = mercantile.xy(bbox[0], bbox[3])
        p2 = mercantile.xy(bbox[2], bbox[1])
    else:
        p1 = (bbox[0], bbox[3])
        p2 = (bbox[2], bbox[1])

    t = [*toImgCoords(p1), *toImgCoords(p2)]
    # print(t)
    return img.crop(t)


# import math

# # Define the bounding box in Web Mercator coordinates
# bbox_web_mercator = bboxes_3857['gauss']
# # 1801162.1345,6126389.5985,1845724.9220,6161053.7909
# # Define the zoom level
# zoom = 17

# # The Earth's semi-circumference in meters
# EARTH_HALF_CIRCUMFERENCE = 20037508.34

# # Define the size of a tile at the given zoom level (in Web Mercator coordinates)
# tile_size = EARTH_HALF_CIRCUMFERENCE * 2 / (2 ** zoom)

# # Calculate the tile indices for the bounding box corners
# min_x_tile = math.floor((bbox_web_mercator[0] + EARTH_HALF_CIRCUMFERENCE) / tile_size)
# max_x_tile = math.ceil((bbox_web_mercator[2] + EARTH_HALF_CIRCUMFERENCE) / tile_size) - 1
# min_y_tile = math.ceil((EARTH_HALF_CIRCUMFERENCE - bbox_web_mercator[3]) / tile_size)
# max_y_tile = math.floor((EARTH_HALF_CIRCUMFERENCE - bbox_web_mercator[1]) / tile_size) - 1

# # Print the tile indices
# print(f'Min x tile: {min_x_tile}, Max x tile: {max_x_tile}')
# print(f'Min y tile: {min_y_tile}, Max y tile: {max_y_tile}')


# # TILE COORDS TO LAT LNG

# import mercantile

# tilematrix=20
# row=363572
# column=571896
# x, y, z = 8738, 5624, 14
# x, y, z = column, row, tilematrix

# # Convert to latitude and longitude
# lnglat = mercantile.ul(x, y, z)

# # Print the latitude and longitude
# print(f'Longitude: {lnglat.lng}, Latitude: {lnglat.lat}')

# bounds = mercantile.xy_bounds(x, y, z)
# print(bounds)