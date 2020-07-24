import datetime
from decimal import Decimal
import requests
from django.conf import settings
import time
import json
from django.utils import timezone

GOOGLE_CLIENT_API = getattr(settings, 'GOOGLE_CLIENT_API', 'AIzaSyCP-MHkDU5D09akZaDdZF_sCM75KoPpPrI')

YELP_AUTH_ENDPOINT = 'https://api.yelp.com/oauth2/token'
YELP_SEARCH_ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
YELP_CLIENT_ID = getattr(settings, 'YELP_CLIENT_ID', 'Wg4dJxSwZ0rf6MQ0x5IDtA')
YELP_CLIENT_SECRET = getattr(settings, 'YELP_CLIENT_SECRET','jcfJM3fnHRwvmXkxYKKnRTDY1SOwWdS8h_8I5PNZ5KQuaHIdH_sOLOKAW5yiRnBSIKby_MiAHdNO2NpiJ_YAaV7i1QkTbHN0H4JNjNQD3o7h9mxdKrFJn0YZoNaCXXYx')

def timestamp_in_past(timestamp_string):
    now = timezone.now() #python datetime
    timestamp_dec = Decimal(timestamp_string) # int("123") / float(123.123)
    timestamp_unaware = datetime.datetime.fromtimestamp(timestamp_dec)
    current_tz = timezone.get_current_timezone()
    timestamp_aware = timezone.make_aware(timestamp_unaware, current_tz)
    if timestamp_aware < now:
        return True # in the past
    return False # not in the past

def get_token(request=None):
    token_exists = False  
    token = None
    # VISE NE TREBA TOKEN U REQUEST NEGO SAMO API KEY
    # if request:
    #     session_token = request.session.get('YELP_TOKEN')
    #     token_expires = request.session.get('YELP_EXPIRES')
    #     if session_token and token_expires:
    #         expired = timestamp_in_past(token_expires)
    #         if not expired:
    #             token_exists = True
    #             token = session_token
    if not token_exists:
        params = {
            'grant_type': 'OAUTH2',
            'client_id': YELP_CLIENT_ID,
            'client_secret': YELP_CLIENT_SECRET
        }
        r = requests.post(YELP_AUTH_ENDPOINT, params=params)
        print(r.text)
        token = r.json()
        # expires = r.json()['expires_in'] #seconds
        # if request:
        #     request.session['YELP_TOKEN'] = token
        #     expires_in = (timezone.now() + datetime.timedelta(seconds=expires))
        #     expires_in_tstamp = expires_in.timestamp()
        #     request.session['YELP_EXPIRES'] = str(expires_in_tstamp)
        #     request.session.set_expiry(expires - datetime.timedelta(days=1).seconds)
    return token


def yelp_search(keyword='Food', location='Newport Beach',lat="40.6971494", lng="-74.2598644", request=None,categories=None):
    # token = get_token(request=request)
    headers = {"Authorization": "Bearer " + YELP_CLIENT_SECRET}
    latitude=lat
    longitude=lng
    params = {'term': keyword, 'location': location,'latitude':latitude,'longitude':longitude,'categories':categories,'locale':'es_MX'}
    r = requests.get(YELP_SEARCH_ENDPOINT, headers=headers, params=params)
    # print(r.status_code)
    return r.json()


class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types,keyword):
            endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            places = []
            params = {
                'location': location,
                'radius': radius,
                'types': types,
                'keyword':keyword,
                'key': self.apiKey
            }
            
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            print("res.status_code:")
            print(res.status_code)
            print("results")
            print(results)   
            
            # return res.json() 
            # places.extend(results['results'])
            # time.sleep(2)
            # while "next_page_token" in results:
            #     params['pagetoken'] = results['next_page_token'],
            #     res = requests.get(endpoint_url, params = params)
            #     results = json.loads(res.content)
            #     places.extend(results['results'])
            #     time.sleep(2)
            



            return results 
    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        # place_details =  json.loads(res.content)
        return res.json()        
 
locu_api = '9fb8cd70cb34cab8e83690473133f51943b5c93f'
 
