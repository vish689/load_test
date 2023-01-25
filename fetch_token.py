import requests
session = requests.session()

def fetch_token(username, password, clientId, clientSecret):
    core_auth_params = {'grant_type': 'password', 'client_id': clientId,
              'client_secret': clientSecret,
              'username': username, 'password': password}
    # TODO: Login URL
    core_auth_res = session.post(url='https://login.salesforce.com/services/oauth2/token', params=core_auth_params)
    core_json_response = core_auth_res.json()
    coreToken = core_json_response['access_token']
    instanceUrl = core_json_response['instance_url']

    offcore_auth_params = {
        'grant_type': 'urn:salesforce:grant-type:external:cdp',
        'subject_token': coreToken,
        'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token'
    }
    offcore_response = session.post(url=f'{instanceUrl}/services/a360/token', params=offcore_auth_params)
    offcore_json_response = offcore_response.json()
    offcore_access_token = offcore_json_response['access_token']
    offcoreUrl = offcore_json_response['instance_url']

    print('####################################################################')
    print(offcoreUrl)
    print(offcore_access_token)
    print('####################################################################')

if __name__ == '__main__':
    fetch_token('<USERNAME>', '<PASSWORD>', '<CLIENT_ID>', '<CLIENT_SECRET>')
