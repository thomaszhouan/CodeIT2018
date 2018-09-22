import logging
from PIL import Image

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def convert_exif_to_degress(value):
    d = float(value[0][0]) / float(value[0][1])
    m = float(value[1][0]) / float(value[1][1])
    s = float(value[2][0]) / float(value[2][1])
    return d + (m / 60.0) + (s / 3600.0)


def get_gps_from_img(filename):
    img = Image.open(filename)
    logging.info(img)
    meta = img._getexif()[34853]
    logging.info(meta)
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
    logging.info("data sent for evaluation {}".format(data))
    logging.info(data[0])
    logging.info(data[0].get('path'))
    return jsonify({})

