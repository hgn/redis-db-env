#!/usr/bin/python3

import asyncio
import aiohttp
import aiohttp.web
import aioredis


async def get(key):
    conn = await aioredis.create_connection(('localhost', 6379), encoding='utf-8')
    return await conn.execute('get', key)


async def db_set(key, value):
    conn = await aioredis.create_connection(('localhost', 6379), encoding='utf-8')
    return await conn.execute('set', key, value)


async def handle(request):
    ip = await get('.core.ip')
    name = request.match_info.get('name', "")
    text = "Hello, " + name + "\n"
    text += ".core.ip " + ip
    return aiohttp.web.Response(text=text)


async def handle_set(request):
    key = request.match_info.get('key')
    value = request.match_info.get('value')
    if not key or not value:
        return aiohttp.web.Response(text="nope")

    await db_set(key, value)

    return aiohttp.web.Response(text="ok")


app = aiohttp.web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)
app.router.add_get('/api/v1/set/{key}/{value}', handle_set)

aiohttp.web.run_app(app)
