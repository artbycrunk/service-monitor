import logging
import time

from aiohttp import web
from jinja2 import Template

from . import storage

logger = logging.getLogger(__name__)

TEMPLATE = """
<html>
<head>
    <title>Service Monitor</title>
    <meta http-equiv="refresh" content="{{ interval }}">
</head>
<style>
.table-striped tbody tr:nth-of-type(odd) {
    background-color: rgba(0,0,0,.05);
}
.green {
    color: green;
}
.red {
    color: red;
}
</style>

<p>Showing data for {{ records }} urls, status limited to last {{ metric_span }} hour(s)</p>
<p>This page will auto refresh every {{ interval }}s</p>

<table class="table table-striped">
    <thead>
        <tr>
        <th scope="col">#</th>
        <th scope="col">Name</th>
        <th scope="col">URL</th>
        <th scope="col">Status</th>
        </tr>
    </thead>
    <tbody>
    {% for row in rows %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>
            <table>
                {% for status in row[3] %}
                    {% if '200' in status %}
                        <td><span class="green" title="{{status}} @ {{ row[4][loop.index-1] }}">&#10004;</span></td>
                    {% else %}
                        <td><span class="red" title="{{status}}  @ {{ row[4][loop.index-1] }}">&#10006;</span></td>
                    {% endif %}
                {% endfor %}
            </table>
            </td>
        </tr>
    {% endfor %}
    </tbody>
</table>
</html>
"""


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


async def summary(request):
    """Get a summary of urls checked

    Arguments:
        request(obj): aiohttp.Request

    """
    start_time = time.time()
    metric_span = request.app["options"].metric_span
    rows = list()
    try:
        for row in storage.get_summary(metric_span=metric_span):
            pos, name, url, status, timestamp = row
            statuses = status.split(",")
            timestamp = timestamp.split(",")
            rows.append([pos, name, url, statuses, timestamp])
    except Exception as e:
        logger.error("ERROR {0}".format(str(e)))
    finally:
        endtime = time.time() - start_time

    logger.info("Summary built in {time}".format(time=endtime))

    if ("json" in request.query
            or request.content_type == "application/json"):
        res = {}
        for row in rows:
            # pos : [name, url, status, timestamp]
            res[row[0]] = row[1:]
        response = web.json_response(res)
    else:
        interval = request.app["options"].interval

        urls = request.app["urls"]

        template = Template(TEMPLATE)
        output = template.render(
            records=len(urls), metric_span=metric_span,
            interval=interval, rows=rows)
        response = web.Response(text=output, content_type='text/html')

    return response
