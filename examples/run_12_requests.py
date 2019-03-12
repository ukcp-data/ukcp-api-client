from ukcp_api_client.client import UKCPApiClient
import os

api_key = os.environ['API_KEY']
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


cli = UKCPApiClient(api_key=api_key)
base_dir = 'monthly_subsets'


for month in months:

    request_url = 'https://ukclimateprojections-ui.metoffice.gov.uk/wps/Execute?' \
                      'Request=Execute&Identifier=LS3_Subset_01&Format=text/xml&Inform=true&Store=false&' \
                      'Status=false&DataInputs=TemporalAverage={};Area=bbox|474459.24|241777.72|' \
                      '486311.19|246518.35;Collection=land-rcm;ClimateChangeType=absolute;' \
                      'EnsembleMemberSet=land-rcm;DataFormat=csv;TimeSlice=2075|2076;Variable=psl'.format(month)
    
      
    outputs_dir = os.path.join(base_dir, month)
    cli.submit(request_url, outputs_dir=outputs_dir)


