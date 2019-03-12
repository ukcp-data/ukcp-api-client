from ukcp_api_client.client import UKCPApiClient
import os
api_key = os.environ['API_KEY']

cli = UKCPApiClient(outputs_dir='my-outputs', api_key=api_key)

request_url = 'https://ukclimateprojections-ui.metoffice.gov.uk/wps/Execute?' \
                      'Request=Execute&Identifier=LS3_Subset_01&Format=text/xml&Inform=true&Store=false&' \
                      'Status=false&DataInputs=TemporalAverage=jan;Area=bbox|474459.24|241777.72|' \
                      '486311.19|246518.35;Collection=land-rcm;ClimateChangeType=absolute;' \
                      'EnsembleMemberSet=land-rcm;DataFormat=csv;TimeSlice=2075|2076;Variable=psl'

file_urls = cli.submit(request_url)
