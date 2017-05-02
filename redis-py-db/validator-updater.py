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

# now we have one key so the output will be "[b'full stack']"
redis_db.get('full stack')
# output is "b'python'", the key and value still exist in Redis
redis_db.incr('twilio')
# output is "1", we just incremented even though the key did not
# previously exist
redis_db.get('twilio')
# output is "b'1'" again, since we just obtained the value from
# the existing key
redis_db.delete('twilio')
# output is "1" because the command was successful
redis_db.get('twilio')
