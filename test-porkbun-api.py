#!/usr/bin/env python3
"""
Simple test script to debug Porkbun API issues
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

PORKBUN_API_KEY = os.getenv('PORKBUN_API_KEY')
PORKBUN_SECRET_KEY = os.getenv('PORKBUN_SECRET_KEY')
PORKBUN_API_URL = 'https://api.porkbun.com/api/json/v3'

def test_api_connectivity():
    """Test basic API connectivity and authentication"""
    print("Testing Porkbun API connectivity...")
    print(f"API URL: {PORKBUN_API_URL}")
    print(f"API Key present: {'Yes' if PORKBUN_API_KEY else 'No'}")
    print(f"Secret Key present: {'Yes' if PORKBUN_SECRET_KEY else 'No'}")
    
    if not all([PORKBUN_API_KEY, PORKBUN_SECRET_KEY]):
        print("❌ Missing API credentials!")
        return False
    
    # Test with listAll endpoint (known to work)
    url = f"{PORKBUN_API_URL}/domain/listAll"
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY
    }
    
    try:
        print(f"\nTesting listAll endpoint: {url}")
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get('status') == 'SUCCESS':
            print("✅ API connectivity test passed!")
            domains = data.get('domains', [])
            print(f"Found {len(domains)} domains")
            return domains
        else:
            print("❌ API returned non-success status")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_get_nameservers(domain):
    """Test the getNs endpoint specifically"""
    print(f"\n{'='*50}")
    print(f"Testing getNs endpoint for: {domain}")
    print(f"{'='*50}")
    
    url = f"{PORKBUN_API_URL}/domain/getNs/{domain}"
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY
    }
    
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            data = response.json()
            print(f"JSON Response: {json.dumps(data, indent=2)}")
        except:
            print(f"Raw Response: {response.text}")
            
        if response.status_code == 400:
            print("\n🔍 400 Bad Request Analysis:")
            print("This could mean:")
            print("1. The getNs endpoint doesn't exist or has changed")
            print("2. The domain doesn't support this operation")
            print("3. API access isn't enabled for this domain")
            print("4. The request format is incorrect")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_alternative_endpoints(domain):
    """Test alternative ways to get nameserver info"""
    print(f"\n{'='*50}")
    print(f"Testing alternative endpoints for: {domain}")
    print(f"{'='*50}")
    
    # Test some possible alternative endpoints
    endpoints_to_try = [
        f"/domain/getNameServers/{domain}",
        f"/domain/ns/{domain}",
        f"/domain/nameservers/{domain}",
        f"/domain/info/{domain}",
        f"/domain/details/{domain}"
    ]
    
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY
    }
    
    for endpoint in endpoints_to_try:
        url = f"{PORKBUN_API_URL}{endpoint}"
        print(f"\nTrying: {url}")
        
        try:
            response = requests.post(url, json=payload)
            print(f"  Status: {response.status_code}")
            
            if response.status_code != 404:
                try:
                    data = response.json()
                    print(f"  Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"  Raw: {response.text[:200]}...")
        except Exception as e:
            print(f"  Error: {e}")

def main():
    print("Porkbun API Debug Tool")
    print("=" * 30)
    
    # Test basic connectivity
    domains = test_api_connectivity()
    
    if not domains:
        print("Cannot proceed - API connectivity failed")
        return
    
    # Pick the first domain for testing
    if domains:
        test_domain = domains[0].get('domain')
        print(f"\nUsing domain for testing: {test_domain}")
        
        # Test the problematic getNs endpoint
        test_get_nameservers(test_domain)
        
        # Test alternative endpoints
        test_alternative_endpoints(test_domain)
        
        print(f"\n{'='*50}")
        print("SUMMARY")
        print(f"{'='*50}")
        print("If getNs endpoint fails with 400, it might mean:")
        print("1. You need to enable API access for each domain in Porkbun dashboard")
        print("2. The endpoint has changed or been deprecated")
        print("3. Your domain doesn't support nameserver management via API")
        print("\nNext steps:")
        print("1. Check Porkbun dashboard -> Domain Management -> API Access")
        print("2. Enable API access for the specific domain")
        print("3. Try the script again")

if __name__ == '__main__':
    main()
