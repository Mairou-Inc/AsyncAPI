from aiohttp import web
import argparse
import requests

URL_WEATHER_SERVICE = 'https://wttr.in/'

parser = argparse.ArgumentParser(description='aiohttp server')
parser.add_argument('--port')
args = parser.parse_args()

def get_request_to_wttr_in():
    response = requests.get(URL_WEATHER_SERVICE)
    return response.text


async def mainpage(request):
    return web.FileResponse('api/index.html')

async def test(request):
    name = request.rel_url.query.get('name')
    return web.Response(text=f"{request.rel_url.query_string}")


async def exponentiation(request):
    try:
        a = int(request.rel_url.query.get('a'))
        b = int(request.rel_url.query.get('b'))
        return web.json_response({'result':a**b})
    except:
        return web.json_response({'error':'not enough parameters'})

async def weather(request):
    return web.Response(
        text=get_request_to_wttr_in(),
        content_type='text/plain',
        charset='utf-8'
    )
  

async def exchange(request):
    return web.json_response


app = web.Application()
app.add_routes([
    web.get('/', mainpage),
    web.get('/test', test),
    web.get('/ex', exponentiation),
    web.get('/weather', weather),
    web.get('/exchange', exchange),
])

web.run_app(app, host='127.0.0.1', port=args.port)


