"""
client.py
=========

Holds the main client class: UKCPApiClient
"""

import os
import re
import logging
import requests

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from ukcp_api_client.utils import (validate_api_key, get_status_url,
        poll_until_ready, get_status_and_message, get_file_urls,
        save_url_to_local_file, FAILED_STATUS)


class UKCPApiClient(object):
    """
    Main client class: UKCPApiClient.

    Usage:
    >>> from ukcp_api_client.client import UKCPApiClient
    >>> cli = UKCPApiClient(outputs_dir='my-outputs', api_key='foobaa')
    >>> request_url = 'https://ukclimateprojections-ui.metoffice.gov.uk/wps?' \
                    'Request=Execute&Identifier=LS3_Subset_01&Format=text/xml&Inform=true&Store=false&' \
                    'Status=false&DataInputs=TemporalAverage=jan;Area=bbox|474459.24|241777.72|' \
                    '486311.19|246518.35;Collection=land-rcm;ClimateChangeType=absolute;' \
                    'EnsembleMemberSet=land-rcm;DataFormat=csv;TimeSlice=2075|2076;Variable=psl'
    >>> file_urls = cli.submit(request_url)
    """

    def __init__(self, outputs_dir='/tmp', api_key=None):
        """
        Constructor for UKCPApiClient class:
        Takes inputs and saves the settings for:

        - outputs_dir
        - api_key

        :param outputs_dir: Output directory to write outputs [directory path]
        :param api_key: API Key [string]
        """
        self._api_key = None
        self._outputs_dir = None

        self.set_api_key(api_key)
        self.set_outputs_dir(outputs_dir)

    def set_api_key(self, api_key):
        """
        Validates and set the API Key for the client.

        :param api_key: API Key [String]
        :return: None
        """
        api_key = api_key or os.environ.get('API_KEY', None)

        if not api_key:
            raise Exception('Must provide API KEY to client:\n'
                            '\tas API_KEY environment variable\n'
                            '\tor as only argument to UKCPAPIClient(...) call')

        validate_api_key(api_key)
        self._api_key = api_key

    def set_outputs_dir(self, outputs_dir):
        """
        Sets the outputs directory for saving output files.
        Creates the directory if it does not exist.

        :param outputs_dir: Output directory to write outputs [directory path]
        :return: None
        """
        if not os.path.isdir(outputs_dir):
            os.makedirs(outputs_dir)

        self._outputs_dir = outputs_dir

    def submit(self, request_url, outputs_dir=None):
        """
        Method for submitting a request to the UKCP API.
        Request (`request`) must be a valid request URL.
        Returns a tuple of (<status>, <response>, <outputs>), where:

        <status> - is a string showing the status returned from the UKCP service.
        <response> - response XML document from server.
        <outputs> - list of output files saved to specified outputs directory.

        :param request_url: UKCP API Request URL [String]
        :param outputs_dir: Output directory to write outputs [directory path]
        :return: tuple of (status, response, outputs)
        """
        # Check correct API Key is in URL
        if 'ApiKey=' in request_url:
            request_url = re.sub('ApiKey=.{32}', 'ApiKey={}'.format(self._api_key), request_url)
        else:
            request_url += '&ApiKey={}'.format(self._api_key)

        if outputs_dir:
            self.set_outputs_dir(outputs_dir)

        # Submit request and get Execute Response XML doc
        log.info('Submitting request with URL: {}'.format(request_url))
        response = requests.get(request_url)

        # Get status URL
        status_url = get_status_url(response.text)

        # Poll until a known status is found
        status, xml = poll_until_ready(status_url)

        # Respond to failure if it failed
        if status == FAILED_STATUS:
            return self._respond_to_failure(xml, request_url)

        # Save the outputs
        output_files = self._save_outputs(xml)

        return status, xml, output_files

    def _respond_to_failure(self, xml, request_url):
        """
        Provide some output information when job has failed.

        :param xml: XML Response Document [String]
        :param request_url: UKCP Request URL [String]
        :return: None
        """
        _, message = get_status_and_message(xml)
        raise Exception('Failed to process request: {}\nThe process failed with error message: "{}"'
                        .format(request_url, message))

    def _save_outputs(self, xml):
        """
        Download the output files and save them to the specified outputs directory.

        :param xml: XML Response Document [String]
        :return: List of local output file paths
        """
        file_urls = get_file_urls(xml)
        outputs = []

        log.info('Saving outputs to:')
        for url in file_urls:

            # Get target file path
            try:
                # Old URL format
                file_name = re.search('fileName=([^&]+)', url).group(1)
            except Exception:
                # New URL format
                file_name = os.path.basename(url)

            target = os.path.join(self._outputs_dir, file_name)

            # Append API Key to URL
            full_url = '{}?ApiKey={}'.format(url, self._api_key)

            log.info("  - {}".format(target))
            save_url_to_local_file(full_url, target)

            outputs.append(target)

        return outputs

