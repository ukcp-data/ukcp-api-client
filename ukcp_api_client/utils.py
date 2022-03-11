"""
utils.py
========

Utility functions and objects for API client.

"""

import time
import re
import logging
import shutil
import xml.etree.ElementTree as ET

import requests

LOG_FORMAT = '%(asctime)-12s %(module)-10s %(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


KNOWN_STATUS_VALUES = ('ProcessAccepted', 'ProcessStarted', 'ProcessSucceeded', 'ProcessFailed')
FINAL_STATUS_VALUES = ('ProcessSucceeded', 'ProcessFailed')
FAILED_STATUS = 'ProcessFailed'

# Element Tree uses qualified namespaces for XML search, so define it
NS = '{http://www.opengeospatial.net/wps}'
OWS_NS = '{http://www.opengeospatial.net/ows}'
OWS_ERROR_NS = '{http://www.opengis.net/ows/1.1}'
POLLING_PAUSE = 2


def validate_api_key(api_key):
    """
    Checks format of API key looks correct.
    Raises Exception if key is incorrectly formatted.

    :param api_key: API Key [string]
    :return: None
    """
    if len(api_key) != 32:
        raise Exception('API Key must be 32 characters long.')

    if re.search('[^A-Za-z0-9\-_]', api_key) or api_key[0] in '-_' or api_key[-1] in '-_':
        raise Exception('API Key must only contain letters, numbers and "-", "_".'
                        ' Must begin and end with a letter or number.')


def get_status_url(xml):
    """

    :param xml: XML Response Document [String]
    :return:
    """
    log.debug('XML Response: \n{}'.format(xml))
    root = ET.fromstring(xml)
    status_url = root.get('statusLocation', None)

    if not status_url:
        # Attempt to get error message
        try: 
            message = next(root.iter(OWS_ERROR_NS + 'ExceptionText')).text
        except Exception:
            message = ('Could not get status URL from response.')

        raise Exception('Request failed: {}'.format(message))

    return status_url


def get_status_and_message(xml):
    """
    Searches XML Response document for status information.
    Returns tuple of (status, status_message).

    :param xml: XML Response Document [String]
    :return: Tuple of (status, message)
    """
    root = ET.fromstring(xml)
    qual_status = root.find(NS + 'Status')[0]
    status = qual_status.tag.replace(NS, '')

    # Failed status requires extra work to get message
    if status == FAILED_STATUS:
        message = next(qual_status.iter(OWS_NS + 'ExceptionText')).text
    else:
        message = qual_status.text

    if status not in KNOWN_STATUS_VALUES:
        raise ValueError('Unknown status value: {}'.format(status))

    return status, message


def get_status(xml):
    """
    Searches XML Response document for status information.
    Returns status.

    :param xml: XML Response Document [String]
    :return: status [String]
    """
    status, _ = get_status_and_message(xml)
    return status


def poll_until_ready(status_url):
    """
    Keep polling the URL `status_url` until the XML Response document returns
    a status that can be responded to (i.e. either a success or failure).

    :param status_url: Status URL [String]
    :return: Tuple of (status, xml_doc)
    """
    status, response = None, None

    while status not in FINAL_STATUS_VALUES:
        log.info('Pausing for {} seconds before polling server...'.format(POLLING_PAUSE))
        time.sleep(POLLING_PAUSE)
        response = requests.get(status_url)
        xml = response.text
        status = get_status(xml)

    log.debug('XML:\n{}'.format(xml))
    return status, xml


def get_file_urls(xml):
    """
    Search the XML Response document for a list of File URLs from which the output files
    can be downloaded.
    Returns a list of file URLs.

    :param xml: XML Response Document [String]
    :return: List of file URLs
    """
    root = ET.fromstring(xml)
    file_url_element = NS + 'FileURL'

    file_urls = [file_url.text for file_url in root.iter(file_url_element)]

    if not file_urls:
        raise Exception('Cannot locate file URLs in "<FileURL>" tags.')

    return file_urls


def save_url_to_local_file(url, filepath):
    """
    Download a file from URL `url` and save to local path `filepath`.

    :param url: URL to a file [String]
    :param filepath: Local file path to write the file [String]
    :return: None
    """
    # Get file as stream - to avoid loading all into memory
    response = requests.get(url, stream=True)

    # Open local file for writing
    with open(filepath, "wb") as local_file:
        shutil.copyfileobj(response.raw, local_file)

