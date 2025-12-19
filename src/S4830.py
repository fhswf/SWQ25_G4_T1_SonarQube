import requests

requests.request('GET', 'https://example.domain') # Noncompliant
requests.get('https://example.domain') # Noncompliant
