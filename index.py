# -*- coding: utf-8 -*-

from flask import Flask, request, Response, render_template
import csv
import json
import os
import re

from zips import ZIPS_TO_LNG_LAT


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def success():
    all_zips = request.form['zips'].split("\n")
    heat_map = {}
    for zipcode in all_zips:
        try:
            formatted_zipcode = str(int(zipcode)).zfill(5)
        except ValueError:
            continue

        if not formatted_zipcode in ZIPS_TO_LNG_LAT:
            continue

        if not formatted_zipcode in heat_map:
            heat_map[formatted_zipcode] = {'count': 0, 'lnglat': ZIPS_TO_LNG_LAT[formatted_zipcode]}

        heat_map[formatted_zipcode]['count'] += 1

    context = {'heat_map': heat_map,
                'radius': request.form['radius'],
                'max_opacity': request.form['max_opacity'] }

    return render_template('map.html', **context)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.debug = port == 5000
    app.run(host='0.0.0.0', port=port)