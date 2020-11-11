from aiohttp import web
import argparse
import requests
import jinja2
import aiohttp_jinja2
import json


WEATHER_TOKEN = 'e8cff88ed93e33fb6905387cb4221c6f'
URL_WEATHER_SERVICE = 'http://api.openweathermap.org/data/2.5/weather'

IP_INFO_TOKEN = '0ecd21b12bf3bf'
URL_IP_INFO = 'https://ipinfo.io/'

URL_EXCHANGE_RATES = 'https://api.exchangeratesapi.io/latest'

"""----------------------------------------------"""

parser = argparse.ArgumentParser(description='aiohttp server')
parser.add_argument('--port')
args = parser.parse_args()

"""----------------------------------------------"""

def request_to_weather_api(remote_ip_address):
    city=get_user_data_ip(remote_ip_address)['city']
    parameters = {'q':city, 'appid':WEATHER_TOKEN, 'units':'metric'}
    return json.loads(requests.get(URL_WEATHER_SERVICE, params=parameters).text)

def get_remote_ip(request):
    return request.headers.get('X-FORWARDED-FOR')

def get_user_data_ip(remote_ip_address):
    parameters = {'TOKEN': IP_INFO_TOKEN}
    return json.loads(requests.get((URL_IP_INFO + remote_ip_address), params=parameters).text)
    
def request_to_exchange_rates_api(exchange):
    parameters = {'base': exchange}
    return json.loads(requests.get(URL_EXCHANGE_RATES, params=parameters).text)

"""----------------------------------------------"""

async def mainpage(request):
    context = {'fake_token':'shgeirughberiuhgbaigbewigu'}
    response = aiohttp_jinja2.render_template(
        '/home/www/code/AsyncAPI/api/templates/index.html',
        request,
        context
    )
    return response


async def test(request):
    name = request.rel_url.query.get('name')
    remote_ip_address = get_remote_ip(request)
    ip_data = get_user_data_ip(remote_ip_address)
    weather_data = request_to_weather_api(remote_ip_address)
    return web.Response(text=f"{request.rel_url.query_string}, {remote_ip_address}, {ip_data}, {weather_data}")


async def exponentiation(request):
    try:
        a = int(request.rel_url.query.get('a'))
        b = int(request.rel_url.query.get('b'))
        return web.json_response({'result':a**b})
    except:
        return web.json_response({'error':'not enough parameters'})

async def weather(request):
    return web.json_response(request_to_weather_api(get_remote_ip(request)))
  

async def exchange(request):
    exchange = request.rel_url.query.get('exchange')
    return web.json_response(request_to_exchange_rates_api(exchange))

"""----------------------------------------------"""

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


