
import argparse
from collections import OrderedDict
import csv
import logging
import multiprocessing
import os
import sys

from . import storage, summary, monitor

logger = logging.getLogger(__name__)

LOG_LEVELS = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def parse_args():
    """Argument Parser for various options."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'csv',
        help='Path to csv file with list of url(s)')
    parser.add_argument(
        "-i", "--interval", dest='interval', type=int, default=10,
        help='Interval to check service health,in minutes (default: 10 min)')
    parser.add_argument(
        "-ms", "--metric-span", dest='metric_span', type=int, default=1,
        help='Span of time to show metric data, in hours (default: 1 hour)')
    parser.add_argument(
        "--log-level", dest='log_level', default="INFO", choices=LOG_LEVELS, type=str,
        help='Span of time to show metric data, in hours (default: 1 hour)')

    return parser.parse_args()


def get_csv_data(filename):
    """CSV to Dict reader, skip duplicate entries.

    Arguments:
        filename(str): path to csv file.

    Returns:
        Dict: [id] -> [pos, name, url]

    """
    urls = OrderedDict()

    if not os.path.exists(filename):
        logger.error("Not a valid csv file: {0}".format(filename))
        return urls

    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0 and row[0] == "name":
                line_count += 1
                continue
            if not row[1]:
                line_count += 1
                continue
            clean_row = [_row.strip() for _row in row]
            _id = ":".join(clean_row)  # keys are unique rows
            urls[_id] = [line_count] + clean_row
            line_count += 1
    return urls


def serve(urls, options):
    """Serve summary via a http server, using multiprocessing.

    Arguments:
        urls(dict): dict converted from csv.
        options(object): options passed to the service.

    """
    process = multiprocessing.Process(
        target=summary.serve_forever, args=(urls, options))
    process.daemon = True
    process.start()


def main():
    """Main function."""

    options = parse_args()

    if options.log_level:
        logging.basicConfig(stream=sys.stdout, level=LOG_LEVELS[options.log_level])

    storage.create_table()
    if not options.csv:
        logger.error("Please provide a valid csv file")
        return

    urls = get_csv_data(options.csv)
    if urls:
        options.interval = 60 * int(options.interval)
        logger.info("Current interval is set at {0}".format(options.interval))

        logger.info("Found {count} urls to process!".format(count=len(urls)))
        serve(urls, options)
