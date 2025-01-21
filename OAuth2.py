import requests

auth_url = "https://www.strava.com/oauth/authorize"
params = {
    'client_id': 'your_client_id',
    'redirect_uri': 'http://localhost',
    'response_type': 'code',
    'scope': 'read_all,profile:read_all,activity:read_all'
}

print(f"Open this URL: {auth_url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type={params['response_type']}&scope={params['scope']}")

# Get the full URL from user
full_url = input("Enter the code from the URL: ")

# Extract the code from the URL
import re
code_match = re.search(r'code=([^&]+)', full_url)
if code_match:
    code = code_match.group(1)
else:
    raise ValueError("Code not found in URL")

token_url = "https://www.strava.com/oauth/token"
token_params = {
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret',  
    'code': code,
    'grant_type': 'authorization_code'
}

response = requests.post(token_url, data=token_params)
tokens = response.json()
print(f"Your refresh token is: {tokens['refresh_token']}")
