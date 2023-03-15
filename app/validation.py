import requests

def send_email_validation_request(email_address: str):
    try:
        response = requests.get(
        f'https://emailvalidation.abstractapi.com/v1/?api_key=16f60603955549f789e0978fb1a87ff2&email={email_address}')
        return response.content
    except requests.exceptions.RequestException as api_error:
        print(f'There was an error contacting the Email Validation API: {api_error}')
        raise SystemExit(api_error)
