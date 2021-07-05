from flask import Flask, render_template, abort, session, redirect, request
from os import urandom
import json
import urllib
import requests as Requests

with open('api-keys.json') as f:
    apiKeys = json.load(f)
with open('client_secret.json') as f:
    googleApiKeys = json.load(f)['web']

app = Flask(__name__)
app.secret_key = urandom(16)


@app.route('/oauth2')
def index():
    app.logger.info('Oauth2 Init:')

    session['state'] = urandom(6)
    
    app.logger.info(session['state']) 

    print(apiKeys['base_url'] + '/oauth2/confirmed')

    Oauth2Params = {    'response_type':'code',
                        'client_id': apiKeys['client_id'],
                        'redirect_uri': apiKeys['base_url'] + '/oauth2/confirmed',
                        'scope':'email',
                        #'state': session['state'] 
                        }
    
    return redirect(apiKeys['auth_uri'] + '?' + urllib.parse.urlencode(Oauth2Params))

@app.route('/oauth2/end')
def hello():
    app.logger.info(request.args)
    app.logger.info(request.data)
    
    
    return 'endOfAuth'

@app.route('/request-mail')
def reqEmail():
    Requests.get()

@app.route('/oauth2/confirmed')
def confirmed():
    
    app.logger.info('----------- OAuth2 confirmed ------------')
    app.logger.info(str(session['state']) + ' ?= ' + str(request.args.get('state')))
    
    app.logger.debug('code = ' + request.args.get('code'))

    # Verify its the same one as the sent.
    if request.args.get('state') != session['state']: abort(401)

    # Store the code!
    session['code'] = request.args.get('code') # The code !
    
        
    data={  'grant_type'    :'authorization_code',
            'client_id'     : apiKeys['client_id'],
            'client_secret' : apiKeys['client_secret'],
            'redirect_uri'  : apiKeys['base_url'] + '/oauth2/confirmed',
            'code'          : session['code']
    }

    r = Requests.post(apiKeys['token_uri'], data=data)

    app.logger.info('--------Content-------')
    app.logger.info(r.status_code)
    app.logger.info(r.text)
    


    
    
    return 'ok'
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    
