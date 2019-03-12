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
git clone https://github.com/agstephens/ukcp-api-client
cd ukcp-api-client
pip install -r requirements.txt
```

Set the `API_KEY` environment variable:

```
export API_KEY=...your_api_key...
```

Run the simple test:

```
python run_1_request.py
```

## API Request Workflow

The following diagram explains the workflow for API Requests:

![alt text](https://github.com/agstephens/ukcp-api-client/raw/master/doc/images/api_flowchart.png "API Flowchart")



