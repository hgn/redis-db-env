#!/usr/bin/python3

import sys
import redis
import json


redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)


with open('db-scheme-001.json') as fd:
    data = json.load(fd)


d = redis_db.keys()

for entry in data['data']:
    name = entry['key']
    avail = redis_db.get(name)
    if not avail:
        print("new database entry, add default value")
        value = entry['data']

        redis_db.set(name, value)
        redis_db.set("{}.meta.date-added",    "2016-01-01.011")
        redis_db.set("{}.meta.last-modified", "2017-01-01.011")

        if data['validation']:
            redis_db.set("{}.meta.validation", data['validation'])


while True:
    # validation phase
    for entry in data['data']:
        avail = redis_db.get(entry['key'])
        if not avail:
            print("error")
            continue
        val = redis_db.get(entry['validation'])
        if val:
            exec(avail['validation'])

sys.exit(0)

redis_db.set('full stack', 'python')
redis_db.keys()

