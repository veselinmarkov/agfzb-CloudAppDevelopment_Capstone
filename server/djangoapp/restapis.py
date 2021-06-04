import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
from . import nlu_sercrets

class RestException(Exception):
    pass

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print('GET from {}'.format(url))
    if 'api_key' in kwargs:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, 
        auth=HTTPBasicAuth('apikey', kwargs['api_key']))
    else:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    status_code = response.status_code
    print('With status {}'.format(status_code))
    if status_code !=200:
        raise RestException('the call to url: {} return status {} message: {}'.format(url, status_code, response.text))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print('Posting json payload {}'.format(json_payload))
    response = requests.post(url, headers={'Content-Type': 'application/json'}, params=kwargs, json=json_payload)
    if response.status_code != 200:
        raise RestException('the call to url: {} return status {} message: {}'.format(url, status_code, response.text))
    return response.text

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a CarDealer object list
    result = []
    json_result = get_request(url)
    if 'docs' in json_result:
        dealers = json_result['docs']
        for dealer in dealers:
            result.append(CarDealer(dealer))
    return result

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a DealerView object listresult = []
    result = []
    json_result = get_request(url, dealerid=dealerId)
    if 'docs' in json_result:
        reviews = json_result['docs']
        for review in reviews:
            #print('Create DealerReview:' +str(review))
            if 'review' in review:
                review['sentiment'] = analyze_review_sentiments(review['review'])
            result.append(DealerReview(review))
    return result


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    print('analyze ' +text)
    params = {}
    params['text'] = text
    #params['version'] = '2019-07-12'
    params['features'] = {"sentiment": {}}
    if 'API_KEY' in os.environ:
        api_key = os.environ['API_KEY']
    else:
        api_key = nlu_secrets.params['api_key']
    if 'API_URL' in os.environ:
        url = os.environ['API_URL']
    else:
        url = nlu_secrets.params['NLU_url']
    #print(params)
    response = requests.post(url, headers={'Content-Type': 'application/json'}, 
        json=params, auth=HTTPBasicAuth('apikey', api_key))
    if response.status_code == 422:
        return response.text
    try:
        label = response.json()['sentiment']['document']['label']
    except Exception:
        raise RestException('Abnormal return from NLU with params:'+response.text)
    return label
