import logging
import urllib.request
from PIL import Image
from io import BytesIO

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def convert_exif_to_degress(value):
    d = float(value[0][0]) / float(value[0][1])
    m = float(value[1][0]) / float(value[1][1])
    s = float(value[2][0]) / float(value[2][1])
    return d + (m / 60.0) + (s / 3600.0)


def get_gps_from_img(filename):
    img = Image.open(filename)
    logging.debug(img)
    meta = img._getexif()[34853]
    logging.debug(meta)
    latitude_ref = meta[1]
    latitute = meta[2]
    longitude_ref = meta[3]
    longitude = meta[4]
    latitute = convert_exif_to_degress(latitute)
    if latitude_ref != 'N':
        latitute = -latitute
    longitude = convert_exif_to_degress(longitude)
    if longitude_ref != 'E':
        longitude = -longitude
    return {'lat': latitute, 'long': longitude}


@app.route('/imagesGPS', methods=['POST'])
def photo_gps():
    data = request.get_json()
    logging.debug("data sent for evaluation {}".format(data))
    result = []
    for item in data:
        url = item.get('path')
        byte = urllib.request.urlopen(url).read()
        f = BytesIO(byte)
        result.append(get_gps_from_img(f))
    return jsonify(result)

