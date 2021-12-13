import httplib2
import argparse
import datetime
from colorama import init
init()
from colorama import Fore

HTTP_SUCCESS = [100, 101, 200, 201, 202, 203, 204, 205, 206, 207, 208]
HTTP_REDIRECT = [300, 301, 302, 303, 304, 307, 308]
HTTP_FAILED = [404, 406, 410, 412, 424, 429, 440, 500, 501, 502, 503, 504, 522]
HTTP_SSL_CERT_REQUIRED = [423, 496]
HTTP_FORBIDDEN = [403]
HTTP_AUTH = [401]
HTTP_BAD_REQUEST = [400, 415, 508]

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--domain', action="store", help="Domain to scan", default=None)
parser.add_argument('-w', '--wordlist', action="store", help="Wordlist to use", default=None)
#parser.add_argument('-c', '--cookie', action="store", help="Session cookie", default=None)
parser.add_argument('-u', '--ua', action="store", help="User agent to set", default="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0")
parser.add_argument('-o', '--outfile', action="store", help="Output file", default="results.txt")

args = vars(parser.parse_args())

headers = {}
headers['User-Agent'] = args['ua']

outputfile = open(args['outfile'], 'w')

h = httplib2.Http()

def getURL(host, directory):
    url = host+directory
    request = h.request(url,headers=headers)[0]
    if request.status in HTTP_SUCCESS:
        print (Fore.LIGHTGREEN_EX + "[+] " + str(request.status) + " OK: " + line.rstrip() + Fore.RESET)
        outputfile.write(str("200: "+host+line))
    elif request.status in HTTP_FAILED:
        print(Fore.LIGHTRED_EX + "[-] " + str(request.status) + " Not Found page: "+ line.rstrip() + Fore.RESET)
    elif request.status in HTTP_BAD_REQUEST:
        print(Fore.LIGHTBLUE_EX + "[-] " + str(request.status) + " Bad Request: "+ line.rstrip() + Fore.RESET)
    elif request.status in HTTP_FORBIDDEN or HTTP_AUTH:
        print(Fore.LIGHTMAGENTA_EX + "[+] " + str(request.status) + " Forbidden: " + line.rstrip() + Fore.RESET)
        outputfile.write(str("403: "+host+line))
    elif request.status in HTTP_REDIRECT:
        print(Fore.LIGHTYELLOW_EX + "[+] " + str(request.status) + " redirect: " + line.rstrip() + Fore.RESET)
        outputfile.write(str("302: "+host+line))
    elif request.status in HTTP_SSL_CERT_REQUIRED:
        print(Fore.LIGHTCYAN_EX + "[+] " + str(request.status) + "SSL_CERT_REQUIRED Locked: " + line.rstrip() + Fore.RESET)
        outputfile.write(str("Block: "+host+line))


with open(args['wordlist']) as dirs:
    for line in dirs:
        getURL(args['domain'],str(line).strip())