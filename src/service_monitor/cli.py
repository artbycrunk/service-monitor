import argparse
import logging
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

def main():
    """Main function."""

    options = parse_args()

    if options.log_level:
        logging.basicConfig(stream=sys.stdout, level=LOG_LEVELS[options.log_level])

