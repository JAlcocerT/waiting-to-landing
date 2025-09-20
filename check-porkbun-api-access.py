#!/usr/bin/env python3
"""
Utility script to check which domains have API access enabled
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

def check_api_access_for_domain(domain):
    """Check if a domain has API access enabled by testing the getNs endpoint"""
    url = f"{PORKBUN_API_URL}/domain/getNs/{domain}"
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'SUCCESS':
                return {'enabled': True, 'nameservers': data.get('ns', [])}
            else:
                return {'enabled': False, 'error': data.get('message', 'Unknown error')}
        else:
            try:
                data = response.json()
                message = data.get('message', 'Unknown error')
            except:
                message = response.text
            return {'enabled': False, 'error': message}
    except Exception as e:
        return {'enabled': False, 'error': str(e)}

def main():
    print("Porkbun API Access Checker")
    print("=" * 40)
    
    if not all([PORKBUN_API_KEY, PORKBUN_SECRET_KEY]):
        print("❌ Missing Porkbun API credentials in .env file")
        return
    
    # Get all domains
    url = f"{PORKBUN_API_URL}/domain/listAll"
    payload = {
        'apikey': PORKBUN_API_KEY,
        'secretapikey': PORKBUN_SECRET_KEY
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'SUCCESS':
            print("❌ Failed to retrieve domains")
            return
            
        domains = data.get('domains', [])
        print(f"Found {len(domains)} domains in your account\n")
        
        enabled_domains = []
        disabled_domains = []
        
        for domain_info in domains:
            domain = domain_info.get('domain')
            print(f"Checking {domain}... ", end="", flush=True)
            
            access_info = check_api_access_for_domain(domain)
            
            if access_info['enabled']:
                print("✅ API Access ENABLED")
                ns_count = len(access_info.get('nameservers', []))
                if ns_count > 0:
                    print(f"   Current nameservers ({ns_count}):")
                    for i, ns in enumerate(access_info['nameservers'], 1):
                        print(f"     {i}. {ns}")
                else:
                    print("   Using default Porkbun nameservers")
                enabled_domains.append(domain)
            else:
                print("❌ API Access DISABLED")
                error = access_info.get('error', 'Unknown error')
                if "not opted in" in error.lower():
                    print("   Reason: Domain not opted in to API access")
                else:
                    print(f"   Reason: {error}")
                disabled_domains.append(domain)
            print()
        
        # Summary
        print("=" * 40)
        print("SUMMARY")
        print("=" * 40)
        print(f"✅ Domains with API access enabled: {len(enabled_domains)}")
        for domain in enabled_domains:
            print(f"   • {domain}")
        
        print(f"\n❌ Domains with API access disabled: {len(disabled_domains)}")
        for domain in disabled_domains:
            print(f"   • {domain}")
        
        if disabled_domains:
            print(f"\n📋 To enable API access for disabled domains:")
            print(f"1. Go to https://porkbun.com/account/domainsSpeedy")
            print(f"2. For each disabled domain:")
            print(f"   - Click 'Details' next to the domain")
            print(f"   - Find the 'API Access' section")
            print(f"   - Enable 'API Access'")
            print(f"3. Wait a few minutes for changes to take effect")
            print(f"4. Run this script again to verify")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
