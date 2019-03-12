# ukcp-api-client

The purpose of the UKCP API Client library is to provide some simple Python tools
that allow users to interact with the UKCP Service interface.

## Pre-requisite

Please ensure that you have signed up for a UKCP User Interface (UI) account pryor
to using the API. You will need to copy your API Key from your user home page before 
being able to submit requests programmatically.

## Getting started

Install the library with:

```
$ git clone https://github.com/ukcp-data/ukcp-api-client
$ cd ukcp-api-client
```

Install dependencies:

```
$ pip install -r requirements.txt
```

Set the `API_KEY` environment variable (on Linux/Mac):

```
$ export API_KEY="hGIG234234g7sNOHWLof982LOSHL34g7"
```

Run the simple test:

```
$ python examples/run_1_request.py
```

## Working with the client library

Here is a simple example of some python code to make a request to the UI.

```
>>> from ukcp_api_client.client import UKCPApiClient
>>> cli = UKCPApiClient(outputs_dir='my-outputs', api_key='foobaa')
>>> request_url = 'https://ukclimateprojections-ui.metoffice.gov.uk/wps/Execute?' \
                  'Request=Execute&Identifier=LS3_Subset_01&Format=text/xml&Inform=true&Store=false&' \
                  'Status=false&DataInputs=TemporalAverage=jan;Area=bbox|474459.24|241777.72|' \
                  '486311.19|246518.35;Collection=land-rcm;ClimateChangeType=absolute;' \
                  'EnsembleMemberSet=land-rcm;DataFormat=csv;TimeSlice=2075|2076;Variable=psl'
>>> file_urls = cli.submit(request_url)
```

## API Request Workflow

The UKCP request workflow is complicated. The following diagram explains the workflow for API Requests.

It is useful to study this diagram so that you understand how the API interacts with the remote service.

![alt text](https://github.com/ukcp-data/ukcp-api-client/raw/master/doc/images/api_flowchart.png "API Flowchart")

## Platform support and dependencies

This library has been tested on Linux, Windows and Mac platforms.

The library has been tested with Python2.7 and Python3.7.

## Contact

If you have any feedback please contact: ag.stephens@stfc.ac.uk
