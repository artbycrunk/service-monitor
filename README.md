# service-monitor

Monitor a list of urls periodically.

Features

* Accepts a csv file containing a list of urls and names
* Interval of check is configurable.
* Exposes summary over local port (defaults to 8080)

## Requirements
* Docker and docker-compose

## Getting Started

1. In the project root folder run `docker-compose up --build`
2. By default this will run the server with `./example/sample.csv` this can be changed via the command argument passed in the `docker-compose.yml` file.

## Summary View

The service will also bind to `http://localhost:8080` where
a summary page can be viewed like the below example

![alt text](./images/summary_view.png "summary_page")
* This page will auto refresh based on the interval time,
and one can hover over each sample for the status code/timestamp of the sample.

* If a json response is required one can pass the content type header of "application/json".

## Service Monitor Arguments
These arguments can be passed as command line arguments to service-monitor

### Possible Args:
```
usage: service-monitor [-h] [-i INTERVAL] [-ms METRIC_SPAN] [--log-level {INFO,DEBUG}] csv

positional arguments:
  csv                   Path to csv file with list of url(s)

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Interval to check service health,in minutes (default:
                        10 min)
  -ms METRIC_SPAN, --metric-span METRIC_SPAN
                        Span of time to show metric data, in hours (default: 1
                        hour)
  --log-level {INFO,DEBUG}
                        Span of time to show metric data, in hours (default: 1
                        hour)
```