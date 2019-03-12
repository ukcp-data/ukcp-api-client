import os
import urllib2
import time
import xml.etree.ElementTree as ET

from ukcp_api_client.client import UKCPApiClient


API_KEY = os.environ.get('API_KEY', None)

if not API_KEY:
    raise Exception('Please define environment variable: "API_KEY"')


BASE_URL = 'https://ukclimateprojections-ui.metoffice.gov.uk'

URL_TEMPLATE = ('{base_url}/wps/Execute?'
    'Request=Execute&Identifier={proc_id}&Format=text/xml&Inform=true&Store=false&'
    'Status=false&DataInputs={data_inputs}&ApiKey={api_key}')

REQUEST_INPUTS = {
    'LS1_Plume_01': 
        ('Area=point|245333.38|778933.24;Baseline=b8100;'
        'Collection=land-prob;ColourMode=c;DataFormat=csv;FontSize=m;'
        'ImageFormat=png;ImageSize=1200;LegendPosition=7;PlotType=PDF_PLOT;'
        'Scenario=sres-a1b;TemporalAverage={month};TimeSlice=2050-2069;'
        'TimeSliceDuration=20y;Variable=tasAnom;'),

    'LS1_Maps_01': 
        ('TemporalAverage=jja;Baseline=b8100;Scenario=rcp45;'
        'Area=bbox|-84667.14|-114260.00|676489.68|1230247.30;'
        'SpatialSelectionType=bbox;TimeSliceDuration=20y;DataFormat=csv;'
        'FontSize=m;Collection=land-prob;TimeSlice=2060-2079;'
        'ShowBoundaries=country;Variable=prAnom;ImageSize=1200;ImageFormat=png')
}


def _call_api(proc_id, expect_error_code=-999, **kwargs):

    dct = {}
    dct['proc_id'] = proc_id
    dct['api_key'] = API_KEY
    dct['base_url'] = BASE_URL
    dct['data_inputs'] = REQUEST_INPUTS[proc_id].format(**kwargs)
 
    url = URL_TEMPLATE.format(**dct) 
    print('Calling: {}'.format(url))

    try:
        response = urllib2.urlopen(url)
    except Exception as err:
        if err.code == expect_error_code:
            return err

        raise Exception('Failed with unexpected error: {}\nURL: {}'.format(err, url))

    xml_doc = response.read()
    return url, xml_doc


def _call_api_expect_429(proc_id, **kwargs):
    err = _call_api(proc_id, expect_error_code=429, **kwargs)
    print('Got required error code: 429')


def _call_api_get_status_url(proc_id, **kwargs):
    url, xml_doc = _call_api(proc_id, **kwargs)
    root = ET.fromstring(xml_doc)

    status_url = root.get("statusLocation", None)

    if not status_url:
        raise Exception('Could not get valid response for request: {}'.format(url))

    return status_url
    

def test_12_months_via_api():
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    for month in months:
        # Sleep for long enough for all to run
        _call_api('LS1_Plume_01', month=month)
        time.sleep(30)


def _check_status(xml_doc):
    if xml_doc.find('<ProcessSucceeded>The End</ProcessSucceeded>') > -1:
        return True
    else:
        return False 


def _poll_status_url(status_url):
    # Polls until completion - unless exited

    while 1:
        time.sleep(5)
        response = urllib2.urlopen(status_url)
        xml_doc = response.read()

        if _check_status(xml_doc):
            return xml_doc


def _get_zip_file_url(xml_doc):
    for line in xml_doc.split('\n'):
        if line.find('.zip</FileURL>') > -1:
            zip_url = line.split('>')[1].split('<')[0]
            return zip_url

    raise Exception('Could not find Zip File location')



def _download_output(url):
    # Append API Key
    url += '?ApiKey={}'.format(API_KEY)

    response = urllib2.urlopen(url)
    output = response.read()
        

def test_single_call():
    status_url = _call_api_get_status_url('LS1_Maps_01')    

    assert(status_url.find(BASE_URL) == 0)

    # Wait for completion
    xml_doc = _poll_status_url(status_url)    

    # Check output for zip file URL
    zip_url = _get_zip_file_url(xml_doc)
    
    # Test download
    _download_output(zip_url) 


def test_5_calls():
    # Expect to get turned away

    for i in range(2):
        time.sleep(0.2)
        _call_api_get_status_url('LS1_Maps_01')

    for i in range(3):
        time.sleep(0.2)
        _call_api_expect_429('LS1_Maps_01')


def test_fail_when_running():
    cli = UKCPApiClient(outputs_dir='my-outputs', api_key=API_KEY)

    request_url = 'https://ukclimateprojections-ui.metoffice.gov.uk/wps/Execute?' \
                  'Request=Execute&Identifier=LS3_Subset_01&Format=text/xml&Inform=true&Store=false&' \
                  'Status=false&DataInputs=TemporalAverage=jan;Area=bbox|474459.24|246518.35|' \
                  '474459.24|246518.35;Collection=land-rcm;ClimateChangeType=absolute;' \
                  'EnsembleMemberSet=land-rcm;DataFormat=csv;TimeSlice=2075|2076;Variable=psl'

    try:
        cli.submit(request_url)
    except Exception as err:
        last_line = str(err).split('\n')[-1].strip()
        assert(last_line == 'The process failed with error message: "IndexError= too many indices for array"')


def test_fail_on_submit():
    cli = UKCPApiClient(outputs_dir='my-outputs', api_key=API_KEY)

    request_url = 'https://ukclimateprojections-ui.metoffice.gov.uk/wps/Execute?' \
                  'Request=Execute&Identifier=Rubbish&Format=text/xml&Inform=true&Store=false'

    try:
        cli.submit(request_url)
    except Exception as err:
        assert(str(err) == 'Request failed: InvalidParameterValue: Identifier not found (None)')
