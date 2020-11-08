from aiohttp import web
import argparse


parser = argparse.ArgumentParser(description='aiohttp server')
parser.add_argument('--port')
args = parser.parse_args()
# async def hello(request):
#    return web.Response(
#         text='<h1>Hello!</h1>',
#         content_type='text/html')



async def api(request):
    return web.Response(text='FUUUUUUUUUUUUUUUUUH BLYAAAAAAAAAAAAAAAAAA')



app = web.Application()
app.add_routes([
    web.get('/', api),
])

web.run_app(app, host='127.0.0.1', port=args.port)


