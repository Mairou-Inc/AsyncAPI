from aiohttp import web
import argparse
import requests
import jinja2
import aiohttp_jinja2


WEATHER_TOKEN = 'e8cff88ed93e33fb6905387cb4221c6f'
URL_WEATHER_SERVICE = 'https://api.openweathermap.org/data/2.5/weather'

IP_INFO_TOKEN = '0ecd21b12bf3bf'
URL_IP_INFO = 'https://ipinfo.io'


parser = argparse.ArgumentParser(description='aiohttp server')
parser.add_argument('--port')
args = parser.parse_args()


def get_request_to_weather_api(remote_ip_address):
    city=get_user_data_ip(remote_ip_address)
    parameters = {'TOKEN':WEATHER_TOKEN, 'CITY':city}
    return requests.get(URL_WEATHER_SERVICE, params=parameters).text

def get_user_data_ip(remote_ip_address):
    parameters = {'TOKEN': IP_INFO_TOKEN, 'IP':remote_ip_address}
    return requests.get(URL_IP_INFO, params=parameters).text
    

async def mainpage(request):
    context = {'fake_token':'shgeirughberiuhgbaigbewigu'}
    response = aiohttp_jinja2.render_template(
        'index.html',
        request,
        context
    )
    return response


async def test(request):
    name = request.rel_url.query.get('name')
    remote_ip_address = request.headers.get('X-FORWRDED_FOR')
    ip_data = get_user_data_ip(remote_ip_address)
    weather_data = get_request_to_weather_api(remote_ip_address)
    return web.Response(text=f"{request.rel_url.query_string}, {remote_ip_address}, {ip_data}, {weather_data}")


async def exponentiation(request):
    try:
        a = int(request.rel_url.query.get('a'))
        b = int(request.rel_url.query.get('b'))
        return web.json_response({'result':a**b})
    except:
        return web.json_response({'error':'not enough parameters'})

async def weather(request):
    return web.Response(
        text=get_request_to_weather_api(),
        content_type='text/plain',
        charset='utf-8'
    )
  

async def exchange(request):
    return web.json_response


app = web.Application()

aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('api/templates'))

app.add_routes([
    web.get('/', mainpage),
    web.get('/test', test),
    web.get('/ex', exponentiation),
    web.get('/weather', weather),
    web.get('/exchange', exchange),
])

web.run_app(app,
    host='127.0.0.1',
    port=args.port
)


