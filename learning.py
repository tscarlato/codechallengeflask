#this is just a file where I test functions and learn stuff



# from jwt import PyJWT
# key = "secret"
# jwt = PyJWT
# encoded = jwt.encode(payload = {"some": "payload"}, key = key, algorithm="HS256")

import requests
import json
from secrets import api_auth_token, jwt_secret_key
from utils import parse_date_time

# url = "https://us-central1-interview-d93bf.cloudfunctions.net/widgets?user_id={user_id}"
# headers={'Authorization': 'apikey:api_auth_token'}
# res = requests.get(url, headers )
# print(res.text)  
# #encode({"some": "payload"}, key, algorithm="HS256")
# #print(encoded)

def widgets(type = None, created_start = None, created_end = None):
    url = "https://us-central1-interview-d93bf.cloudfunctions.net/widgets?user_id=1"
    headers = {'Authorization': 'apikey '+api_auth_token, 'Content-Type': 'application/json'}
    query_params = {}
    if type:
        query_params.update({'type': type})
    if created_start:
        query_params.update({'created_start': created_start})
    if created_end:
        query_params.update({'created_end': created_end})   
    if query_params:
        print("query is true")
        query = json.dumps({"query": query_params})
        print(query)
        res = requests.get(url, headers = headers, params = query)
    else:    
        res = requests.get(url, headers = headers)
    res_dict = json.loads(res.content)
    #res = requests.get(url, headers = headers, data = query)
   # print(res.text)
    parsed_result = parse_type(res_dict)

    filter_result(parsed_result, type, created_start, created_end)



def parse_type(res_dict):
    import re
    for item in res_dict:
        type_label = re.sub(r'-', " ", item['type']).title()
        item['type_label'] = type_label
        item['created'] = parse_date_time(item['created'])
    print(type(res_dict))
    return res_dict

def filter_result(parsed_result, type = None, created_start = None, created_end = None):
    filtered_result=[]
    for item in parsed_result:
        if type and item['type'] != type:
            pass
        elif created_start and item['created'] != created_start:
            pass
        elif created_end and item['created'] != created_end:
            pass
        else:
            print(item['type'])
            filtered_result.append(item)
    print(filtered_result)
    return filtered_result



widgets(type = "flugel-horn")