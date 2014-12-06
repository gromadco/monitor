"""
Populates MongoDB with data.
"""

import datetime
import json
import os
import re

from pymongo import MongoClient


db = MongoClient().monitor
db.data.drop()

for dirpath, dirnames, filenames in os.walk('data'):
    for filename in filenames:
        print filename
        if not re.match(r'^\d.*', filename):
            continue
        with open(os.path.join('data', filename)) as f:
            data = json.load(f)
            for d in data:
                date = datetime.datetime.strptime(filename, '%Y-%m-%d.json')
                d['date'] = date
                # id format: <project slug>-<milestone id>-<date>
                d['_id'] = "{}-{}-{}".format(
                    d['project'], d['data'][0]['id'], filename.split('.')[0]
                )
            db.data.insert(data)
