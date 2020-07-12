import asyncio
import functools
import logging
import signal
import time

import aiohttp

from . import storage

logger = logging.getLogger(__name__)

headers = {
    'user-agent': (
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/52.0.2743.60 Safari/537.36'
    )
}


async def get(session, pos, name, url):
    """Request url head and save response to storage.

    Arguments:
        session(obj): aiohttp.ClientSession to use.
        pos(int): the pos of the url in relatioon to the csv.
        name(str): name associated with the url.
        url(str): the url to check.

    Returns:
        Bool: True if the request was valid, else False

    """
    try:
        resp = await session.request('HEAD', url)
        storage.insert_row(name, url, resp.status, pos)
        logger.debug("{0} {1} {2} {3}".format(pos, name, url, resp.status))
    except Exception:
        storage.insert_row(name, url, 'FAIL', pos)
        logger.debug("{0} {1} {2} {3}".format(pos, name, url, 'FAIL'))
        return False
    return True

def process(urls, interval):
    """Fetch all urls at a given interval.

    Arguments:
        urls(dict): dict converted from csv.
        interval(int): time to sleep in between checks

    """
    loop = asyncio.get_event_loop()
    try:
        loop_forever = True

        conn = aiohttp.TCPConnector(verify_ssl=False, limit_per_host=2)
        timeout = aiohttp.ClientTimeout(total=5)
        session = aiohttp.ClientSession(connector=conn, headers=headers, timeout=timeout)

        while loop_forever:
            try:
                tasks = list()
                for _, value in urls.items():
                    pos, name, url = value
                    tasks.append(asyncio.ensure_future(get(session, pos, name, url)))

                loop.run_until_complete(asyncio.gather(*tasks))
            except KeyboardInterrupt:
                loop_forever = False
    except Exception as e:
        logger.error("MAIN LOOP ERROR {0}".format(str(e)))


def start(urls, interval):
    """Main function."""
    process(urls, interval)
