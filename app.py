from time import mktime
from functools import wraps
from flask import Flask, request, jsonify, session, flash, render_template, make_response
import datetime
import jwt
import requests

from secrets import api_auth_token, jwt_secret_key
from utils import parse_date_time
from business import get_user_by_email

app = Flask(__name__)
app.config['SECRET_KEY'] = jwt_secret_key

#TODO still manually adding the token to the url. that seesm wrong.
#TODO clean up code once it all works
#TODO make sure wraps are working and appropriate
#TODO reduce duplication
#TODO comment code

#pretty sure this works as expected
def decode_auth_token(auth_token):
    return jwt.decode(auth_token, app.config['SECRET_KEY'])

#pretty sure this works as expected
def encode_auth_token(user_id, name, email, scope):
    return jwt.encode(
         payload = {
        'sub': user_id,
        'name': name,
        'email': email,
        'scope': scope,
        'exp': mktime((datetime.datetime.now() + datetime.timedelta(days=1)).timetuple())
        },key=app.config['SECRET_KEY'], algorithm="HS256")#.decode("utf-8")

#TODO make this work wih Bearer token auth
def get_user_from_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        #token = request.headers.get('Authorization': 'Bearer <token>')
        token = request.args.get('token')
        if not token:
            return jsonify({'messaage' : 'missing token'}), 403
        try:
            data = decode_auth_token(token, app.config['SECRET_KEY'])
            return data
        except:
            return jsonify({'message': 'invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped

#TODO more testing, seems inconsistent
@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Currently not logged in"

#TODO more testing. not sure if this works properly or is even needed
@app.route('/authorized')
@get_user_from_token
def authorized():
    return 'this is the authorized view, cant get here without a token'


#TODO testing. also: # get the user data from the auth/header/jwt
@app.route('/user', methods=['GET'])
def user():
    token = request.args.get('token')
    try:
        user = jwt.decode(token, app.config['SECRET_KEY'])
    except: 
        return jsonify({'message': "token invald"})
    return {
        'user_id': user['sub'],
        'name': user['name'],
        'email': user['email']
    }

#TODO use flask.request to get the json body and get the email and scopes property
@app.route('/login', methods=['POST'])
def login():
    if request.form['email']:
        user = get_user_by_email(request.form['email'])
        session['logged_in'] = True
        token = encode_auth_token(user_id = user['id'], name = user['name'], email = user['email'], scope=["openid"])
       # return token
        return {'token': token}
    else:
        return make_response("unable to verify user", 403, {'WWW-Authenticate': 'Basic-Realm="Login Required"'})

#API request works, some of the date time stuff doesn't. need to test the route itself
@app.route('/widgets', methods=['GET'])
def widgets(type = None, created_start = None, created_end = None):
    url = "https://us-central1-interview-d93bf.cloudfunctions.net/widgets?user_id={user_id}"
    headers = {'Authorization': 'apikey '+api_auth_token, 'Content-Type': 'application/json'}
    res = requests.get(url, headers = headers, data = query)
    res_dict = json.loads(res.content)
    parsed_result = parse_dict(res_dict)
    filtered_result = filter_result(parsed_result, type, created_start, created_end)
    return {
        'total_widgets_own_by_user': len(filtered_result),
        'matching_items': filtered_result
    }

#TODO fix parse_date_time issue
def parse_dict(res_dict):
    import re
    for item in res_dict:
        type_label = re.sub(r'-', " ", item['type']).title()
        item['type_label'] = type_label
        item['created'] = parse_date_time(item['created'])
    return res_dict

#TODO create_start and create_end need work. I tried removing the item instead of passing but that wasn't working. 
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

if __name__ == '__main__':
    app.run()
  