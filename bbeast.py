#!/usr/bin/env python3
#
# Generate a short URL using bbea.st

import urllib.request
import urllib.parse
import json
import sys
import re
import requests
import logging
import argparse

VERSION = '0.0.4'
API_KEY = None
API_URL = 'https://bbea.st/generate'

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().name = 'bbea.st'
logging.basicConfig(format='%(asctime)s [%(name)s] {%(levelname)s}: %(message)s', datefmt='%m-%d %H:%M')

logger = logging.getLogger()

def fetch(key, url):
    """
    Perform the actual URL shortening
    :param key
    :param url
    """

    if not validate_url(url):
        logger.fatal('Invalid URL format provided: "{}"'.format(url))
        return 1

    try:
        req = requests.post(API_URL, data={
                    'api_key':  key,
                    'url':      url
                }, headers={
                    'User-Agent': 'bbea.st CLI/{} <contact@binarybeast.com>'.format(VERSION)
                }
        )

        # Fail
        if not req.ok or req.status_code != 200:
            logger.fatal('Error resopnse from the server\n\tStatus code: {}, {}\n'.format(req.status_code, req.reason))
            return 1

        # Clean up the connection
        req.close()

        # Process the response
        d = json.loads(req.content.decode('utf-8'))

        logging.info('-- URL Shortened successfully')
        logging.debug('Full Response: {}'.format(d))

        print( d['url_short'] )

    except ConnectionError as e:
        logger.fatal('Connection error ocurred: {}'.format(e))
        return 1

    return 0


def validate_url(url):
    """
    Ensure the provided URL is a valid URL
    """

    if not re.search(r'^https?://[a-z0-9-]+(\.[a-z0-9-]+)+(:[0-9]+)?(/.*)*$', url, re.IGNORECASE):
        return False

    return True

def print_err(msg):
    """
    Print an error message and exit
    """

    logger.fatal('[ERROR] {}'.format(msg))
    sys.exit(1)


def main():

    parser = argparse.ArgumentParser(description='bbea.st URL Shortener')
    parser.add_argument('--key', '-k', default=API_KEY, help='API Key', type=str)
    parser.add_argument('--verbose', '-v', default=False, help='Enable verbose output', action='store_true')
    parser.add_argument('url', type=str, help='URL to parse')

    args = parser.parse_args()

    if not args.key:
        print_err('No API key defined, either provide one with --key or define one at the top of this script')

    if not args.url:
        print_err('No URL provided')

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    sys.exit( fetch(args.key, args.url) )


if __name__ == '__main__':
    main()
