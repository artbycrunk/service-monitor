import logging
import time

from aiohttp import web
from . import storage

logger = logging.getLogger(__name__)

def serve_forever(urls, options):
    """Start an async web server, adding the summary handler.

    Arguments:
        urls(dict): dict converted from csv.
        options(object): options passed to the service.

    """
    app = web.Application()
    app['urls'] = urls
    app['options'] = options
    app.add_routes([web.get('/', summary)])
    web.run_app(app)
