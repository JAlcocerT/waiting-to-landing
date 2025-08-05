#https://kb.porkbun.com/category/38-registration-and-renewals
# https://porkbun.com/api/json/v3/documentation
#https://porkbun.com/api/json/v3/documentation#apiHost

import os
import requests
import json
import questionary
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

PORKBUN_API_KEY = os.getenv('PORKBUN_API_KEY')
PORKBUN_SECRET_KEY = os.getenv('PORKBUN_SECRET_KEY')
PORKBUN_API_URL = 'https://api.porkbun.com/api/json/v3'

def check_domain_availability(domain_name):
    """Checks if a domain is available and gets its price using a single API call."""
    if not all([PORKBUN_API_KEY, PORKBUN_SECRET_KEY]):
        return {'success': False, 'error': 'Missing Porkbun API credentials in .env file.'}

    url = f"{PORKBUN_API_URL}/domain/checkDomain/{domain_name}"
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        if data.get('status') == 'SUCCESS':
            availability = data.get('response', {}).get('avail')
            price = data.get('response', {}).get('price')

            if availability == 'yes':
                return {
                    'success': True,
                    'available': True,
                    'price': price,
                    'currency': 'USD'  # Porkbun API prices are in USD
                }
            else:
                return {'success': True, 'available': False, 'reason': 'Domain is not available'}
        else:
            return {'success': False, 'error': 'Failed to check domain availability.', 'details': data}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e), 'details': e.response.json() if e.response else 'No response'}

def register_domain(domain_name):
    """Registers a domain name."""
    url = f"{PORKBUN_API_URL}/domain/create"
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY,
        'domain': domain_name,
        # Porkbun will use the default contact info from your account.
        # Sending an empty contact object can sometimes resolve API issues.
        'registrantContact': {}
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return {'success': True, 'response': response.json()}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e), 'details': e.response.json() if e.response else 'No response'}

def main():
    """Main function to run the interactive domain tool."""
    print("Porkbun Domain Tool")
    print("-------------------")

    if not all([PORKBUN_API_KEY, PORKBUN_SECRET_KEY]):
        print("\nError: Missing Porkbun API credentials.")
        print("Please add PORKBUN_API_KEY and PORKBUN_SECRET_KEY to your .env file.")
        return

    domain_name = questionary.text("Enter the domain name you want to check (e.g., 'example.com'):").ask()
    if not domain_name or '.' not in domain_name:
        print("Invalid domain name format.")
        return

    print(f"\nChecking availability for {domain_name}...")
    result = check_domain_availability(domain_name)

    if not result.get('success'):
        print(f"\nError: {result.get('error')}")
        if result.get('details'):
            print(f"Details: {json.dumps(result.get('details'), indent=2)}")
        return

    if result.get('available'):
        price = result.get('price')
        print(f"\nGood news! '{domain_name}' is available for registration.")
        print(f"Registration price: ${price} USD for the first year.")
        
        purchase = questionary.confirm(f"Do you want to register '{domain_name}' now for ${price}?", default=False).ask()
        
        if purchase:
            print(f"\nRegistering '{domain_name}'...")
            reg_result = register_domain(domain_name)
            if reg_result.get('success'):
                print("\nRegistration successful!")
                print(json.dumps(reg_result.get('response'), indent=2))
            else:
                print(f"\nRegistration failed: {reg_result.get('error')}")
                if reg_result.get('details'):
                    print(f"Details: {json.dumps(reg_result.get('details'), indent=2)}")
        else:
            print("Registration cancelled.")
    else:
        print(f"\nSorry, '{domain_name}' is not available. Reason: {result.get('reason')}")

if __name__ == '__main__':
    main()