
from StringIO import StringIO
import os
import xml.etree.ElementTree as ET


_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ExecuteResponse xmlns="http://www.opengeospatial.net/wps" xmlns:ows="http://www.opengeospatial.net/ows" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" statusLocation="https://ukclimateprojections-ui.metoffice.gov.uk/status/4aa3b60afa489a11b9772c8a1d956625" version="1.0.0" xsi:schemaLocation="http://www.opengeospatial.net/wps ../wpsExecute.xsd">
	<Process>
		<ows:Identifier>LS1_Maps_01</ows:Identifier>
		<ows:Title>Maps: Anomalies for probabilistic projections (25km) over UK, 1961-2100</ows:Title>
		<ows:Abstract>Generates maps of 10th, 50th and 90th percentiles of future changes over the UK for one variable from the probabilistic projections. Results are available for anomalies for a given scenario, temporal average, time and the 25km grid or regional averages.</ows:Abstract>
	</Process>
	<Status>
			<ProcessSucceeded>The End</ProcessSucceeded>
	</Status>
		<DataInputs>
			<Input>
				<ows:Identifier>Area</ows:Identifier>
				<ows:Title>Area</ows:Title>
				<LiteralValue>bbox,-84667.14,-114260.0,676489.68,1230247.3</LiteralValue>
			</Input><Input>
				<ows:Identifier>Baseline</ows:Identifier>
				<ows:Title>Baseline</ows:Title>
				<LiteralValue>b8100</LiteralValue>
			</Input><Input>
				<ows:Identifier>Collection</ows:Identifier>
				<ows:Title>Collection</ows:Title>
				<LiteralValue>land-prob</LiteralValue>
			</Input><Input>
				<ows:Identifier>DataFormat</ows:Identifier>
				<ows:Title>DataFormat</ows:Title>
				<LiteralValue>csv</LiteralValue>
			</Input><Input>
				<ows:Identifier>FontSize</ows:Identifier>
				<ows:Title>FontSize</ows:Title>
				<LiteralValue>m</LiteralValue>
			</Input><Input>
				<ows:Identifier>ImageFormat</ows:Identifier>
				<ows:Title>ImageFormat</ows:Title>
				<LiteralValue>png</LiteralValue>
			</Input><Input>
				<ows:Identifier>ImageSize</ows:Identifier>
				<ows:Title>ImageSize</ows:Title>
				<LiteralValue>1200</LiteralValue>
			</Input><Input>
				<ows:Identifier>Scenario</ows:Identifier>
				<ows:Title>Scenario</ows:Title>
				<LiteralValue>rcp45</LiteralValue>
			</Input><Input>
				<ows:Identifier>ShowBoundaries</ows:Identifier>
				<ows:Title>ShowBoundaries</ows:Title>
				<LiteralValue>country</LiteralValue>
			</Input><Input>
				<ows:Identifier>SpatialSelectionType</ows:Identifier>
				<ows:Title>SpatialSelectionType</ows:Title>
				<LiteralValue>bbox</LiteralValue>
			</Input><Input>
				<ows:Identifier>TemporalAverage</ows:Identifier>
				<ows:Title>TemporalAverage</ows:Title>
				<LiteralValue>jja</LiteralValue>
			</Input><Input>
				<ows:Identifier>TimeSlice</ows:Identifier>
				<ows:Title>TimeSlice</ows:Title>
				<LiteralValue>2060-2079</LiteralValue>
			</Input><Input>
				<ows:Identifier>TimeSliceDuration</ows:Identifier>
				<ows:Title>TimeSliceDuration</ows:Title>
				<LiteralValue>20y</LiteralValue>
			</Input><Input>
				<ows:Identifier>Variable</ows:Identifier>
				<ows:Title>Variable</ows:Title>
				<LiteralValue>prAnom</LiteralValue>
			</Input>
		</DataInputs>
		<OutputDefinitions>
			<Output>
				<ows:Identifier>LS1_Maps_01</ows:Identifier>
				<ows:Title>Maps: Anomalies for probabilistic projections (25km) over UK, 1961-2100</ows:Title>
				<ows:Abstract>Generates maps of 10th, 50th and 90th percentiles of future changes over the UK for one variable from the probabilistic projections. Results are available for anomalies for a given scenario, temporal average, time and the 25km grid or regional averages.</ows:Abstract>
			</Output>
		</OutputDefinitions>
		<ProcessOutputs>
			<Output>
				<ows:Identifier>LS1_Maps_01</ows:Identifier>
				<ows:Title>Maps: Anomalies for probabilistic projections (25km) over UK, 1961-2100</ows:Title>
				<ows:Abstract>Generates maps of 10th, 50th and 90th percentiles of future changes over the UK for one variable from the probabilistic projections. Results are available for anomalies for a given scenario, temporal average, time and the 25km grid or regional averages.</ows:Abstract>
				 <ComplexValue schema="schema_url" format="text/xml"><WPSResponseDetails>
  
  <JobDetails>
        <JobID>4aa3b60afa489a11b9772c8a1d956625</JobID>
        <JobRequestURL>https://ukclimateprojections-ui.metoffice.gov.uk/wps/Execute?Request=Execute%26Identifier=LS1_Maps_01%26Format=text/xml%26Inform=true%26Store=false%26Status=false%26DataInputs=TemporalAverage=jja;Baseline=b8100;Scenario=rcp45;Area=bbox|-84667.14|-114260.00|676489.68|1230247.30;SpatialSelectionType=bbox;TimeSliceDuration=20y;DataFormat=csv;FontSize=m;Collection=land-prob;TimeSlice=2060-2079;ShowBoundaries=country;Variable=prAnom;ImageSize=1200;ImageFormat=png</JobRequestURL>
        <JobUnixCompletionTime>1551776227.96</JobUnixCompletionTime>
        <JobCompletionTimeDate>2019-03-05 08:57:07.956125</JobCompletionTimeDate>
        <JobSubmissionTime>2019-03-05 08:56:59.293172</JobSubmissionTime>
        <JobCapabilities>download</JobCapabilities>
        <JobDuration>
                6.89381599426
        </JobDuration>
        <JobVolume>179595</JobVolume>
        <RequestDescription>Generates maps of 10th, 50th and 90th percentiles of future changes over the UK for one variable from the probabilistic projections. Results are available for anomalies for a given scenario, temporal average, time and the 25km grid or regional averages.</RequestDescription>
        <RequestType>image async</RequestType>
            <FileSet>
        <FileDetails>
            <FileURL>https://ukclimateprojections-ui.metoffice.gov.uk/dl/0/4aa3b60afa489a11b9772c8a1d956625/output_4aa3b60afa489a11b9772c8a1d956625_20190305_085707.zip</FileURL>
            <FileSize>179595</FileSize>
            <FileInfo>Zip file 1</FileInfo>
            <FileType>zip</FileType>
            <FileCapabilities>download expand_description</FileCapabilities>
            <FileContents>
        <FileDetails>
            <FileURL>https://ukclimateprojections-ui.metoffice.gov.uk/dl/0/4aa3b60afa489a11b9772c8a1d956625/three_maps_2019-03-05T08-57-01.png</FileURL>
            <FileSize>183027</FileSize>
            <FileInfo>Map</FileInfo>
            <FileType>image</FileType>
            <FileCapabilities></FileCapabilities>
            <FileContents/>
        </FileDetails><FileDetails>
            <FileURL>https://ukclimateprojections-ui.metoffice.gov.uk/dl/0/4aa3b60afa489a11b9772c8a1d956625/three_maps_2019-03-05T08-57-07_10.csv</FileURL>
            <FileSize>6495</FileSize>
            <FileInfo>Map data</FileInfo>
            <FileType>data</FileType>
            <FileCapabilities></FileCapabilities>
            <FileContents/>
        </FileDetails><FileDetails>
            <FileURL>https://ukclimateprojections-ui.metoffice.gov.uk/dl/0/4aa3b60afa489a11b9772c8a1d956625/three_maps_2019-03-05T08-57-07_50.csv</FileURL>
            <FileSize>6423</FileSize>
            <FileInfo>Map data</FileInfo>
            <FileType>data</FileType>
            <FileCapabilities></FileCapabilities>
            <FileContents/>
        </FileDetails><FileDetails>
            <FileURL>https://ukclimateprojections-ui.metoffice.gov.uk/dl/0/4aa3b60afa489a11b9772c8a1d956625/three_maps_2019-03-05T08-57-07_90.csv</FileURL>
            <FileSize>5625</FileSize>
            <FileInfo>Map data</FileInfo>
            <FileType>data</FileType>
            <FileCapabilities></FileCapabilities>
            <FileContents/>
        </FileDetails><FileDetails>
            <FileURL>https://ukclimateprojections-ui.metoffice.gov.uk/dl/0/4aa3b60afa489a11b9772c8a1d956625/input_paths.txt</FileURL>
            <FileSize>199</FileSize>
            <FileInfo>Input files</FileInfo>
            <FileType>data</FileType>
            <FileCapabilities></FileCapabilities>
            <FileContents/>
        </FileDetails><FileDetails>
            <FileURL>https://ukclimateprojections-ui.metoffice.gov.uk/dl/0/4aa3b60afa489a11b9772c8a1d956625/data_licence.txt</FileURL>
            <FileSize>146</FileSize>
            <FileInfo>Data licence</FileInfo>
            <FileType>data</FileType>
            <FileCapabilities></FileCapabilities>
            <FileContents/>
        </FileDetails><FileDetails>
            <FileURL>https://ukclimateprojections-ui.metoffice.gov.uk/dl/0/4aa3b60afa489a11b9772c8a1d956625/request.txt</FileURL>
            <FileSize>418</FileSize>
            <FileInfo>Input parameters</FileInfo>
            <FileType>data</FileType>
            <FileCapabilities></FileCapabilities>
            <FileContents/>
        </FileDetails>
            </FileContents>
        </FileDetails>
    </FileSet>
    </JobDetails>
  <ProcessSpecificContent>
</ProcessSpecificContent>
</WPSResponseDetails></ComplexValue>
			</Output>
		</ProcessOutputs>
</ExecuteResponse>"""

_NS = '{http://www.opengeospatial.net/wps}'



def _tmp_xml_file(tmp_dir):
    p = tmp_dir.mkdir('tmpfiles').join('test.xml')
    p.write(_XML)
    return p


def test_parse_xml(tmpdir):
    root = ET.fromstring(_XML)
    assert(root[0][0].text == 'LS1_Maps_01')

    tree = ET.parse(StringIO(_XML))
    root = tree.getroot()
    assert(root[0][0].text == 'LS1_Maps_01')

    p = tmpdir.mkdir('tmpfiles').join('test.xml')
    p.write(_XML)
    tree = ET.parse(p.strpath)
    root = tree.getroot()
    assert(root[0][0].text == 'LS1_Maps_01')


def test_get_status_url():
    root = ET.fromstring(_XML)
    assert(root.get('statusLocation')  == \
      'https://ukclimateprojections-ui.metoffice.gov.uk/status/4aa3b60afa489a11b9772c8a1d956625')


def test_get_status_from_xml():
    root = ET.fromstring(_XML)
    qual_status = root.find(_NS + 'Status')[0].tag
    status = qual_status.replace(_NS, '')

    assert(status == 'ProcessSucceeded') 


def _get_zip_file_url(xml_file):
    root = ET.parse(xml_file).getroot()
    
    file_url_element = _NS + 'FileURL'

    for file_url in root.iter(file_url_element):
        if file_url.text.endswith('.zip'):
            return file_url.text

    raise Exception('Cannot locate zip file url in "<FileURL>" tag')


def test_get_zip_file_url(tmpdir):
    p = tmpdir.mkdir('tmpfiles').join('test.xml')
    p.write(_XML)

    zip_file_url = _get_zip_file_url(p.strpath)

    assert(zip_file_url == 'https://ukclimateprojections-ui.metoffice.gov.uk/dl/0/4aa3b60afa489a11b9772c8a1d956625/output_4aa3b60afa489a11b9772c8a1d956625_20190305_085707.zip')
