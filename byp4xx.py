import grequests, argparse, os, sys, ua_generator, tldextract
from colorama import init, Fore, Style
from pyfiglet import Figlet

# INITIALISE COLORAMA
init()

os.system("cls||clear")

# DISPLAY BANNER -- START
custom_fig = Figlet(font='slant')
print(Fore.CYAN + Style.BRIGHT + custom_fig.renderText('byp4xx') + Style.RESET_ALL)
print(Fore.GREEN + Style.BRIGHT + "____________________ Rizsyad AR ____________________\n")

print(Fore.GREEN + Style.BRIGHT + "GREEN\t\t: 2xx Status Code" + Style.RESET_ALL)
print(Fore.YELLOW + Style.BRIGHT + "YELLOW\t\t: 3xx Status Code" + Style.RESET_ALL)
print(Fore.RED + Style.BRIGHT + "RED\t\t: 4xx Status Code" + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "MAGENTA\t\t: 5xx Status Code" + Style.RESET_ALL)

print("\n")
# DISPLAY BANNER -- END

# HANDLE ARGUMENTS -- START
parser = argparse.ArgumentParser()
parser.add_argument("-U", "--url", type=str, help="single URL to scan, ex: http://example.com", required=True)
parser.add_argument("-D", "--dir", type=str, help="Single directory/path to scan, ex: admin", required=True)
parser.add_argument("-H", '--header', action="store_true", default=False, help="Header Bypass")
parser.add_argument('-C', "--protocol", action="store_true", default=False, help="Protocol Bypass")
parser.add_argument("-P", '--port', action="store_true", default=False, help="Port Bypass")
parser.add_argument("-M", '--method', action="store_true", default=False, help="HTTP Method Bypass")
parser.add_argument('-E', "--encode", action="store_true", default=False, help="URL Encode Bypass")
parser.add_argument("-A", '--all', action="store_true", default=False, help="ALL BYPASSES")
# parser.add_argument("-U", "--urllist", type=str, help="path to list of URLs, ex: urllist.txt")
# parser.add_argument("-D", "--dirlist", type=str, help="path to list of directories/paths, ex: dirlist.txt")

args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
# HANDLE ARGUMENTS -- END

def createfile(results, url):
   domain = tldextract.extract(url).domain

   with open(f"output_{domain}.txt", "a") as file:
      for line in results:
         file.write(line + "\n")

def printout(url, method, header, status_code, length):
   results = []

   if status_code == 200 or status_code == 201:
      colour = Fore.GREEN + Style.BRIGHT
   elif status_code == 301 or status_code == 302:
      colour = Fore.YELLOW + Style.BRIGHT
   elif status_code == 403 or status_code == 404:
      colour = Fore.RED + Style.BRIGHT
   elif status_code == 500:
      colour = Fore.MAGENTA + Style.BRIGHT
   else:
      colour = Fore.WHITE + Style.BRIGHT

   target_address = f"{method} --> " + url
   info = f"STATUS: {colour}{status_code}{Style.RESET_ALL}\tSIZE: {length}"
   info_pure = f"STATUS: {status_code}\tSIZE: {length}"
   remaining = 100 - len(target_address)

   print("\n" + target_address + " " * remaining + info)
   print(f"Header= {header}")

   results.append("\n" + target_address + " " * remaining + info_pure + f"\nHeader= {header}")
   createfile(results, url)
  
def printresponse(responses):
   for response in responses:
      if response is None:
         continue

      printout(response.request.url, response.request.method, response.request.headers, response.status_code, response.headers.get('Content-Length'))

def headerBypass(url, path):
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)
   print(Fore.CYAN + Style.BRIGHT + "[+] HTTP Header Bypass" + Style.RESET_ALL)
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)

   headers = [line.rstrip() for line in open("payload/headers.txt")]
   ips = [line.rstrip() for line in open('payload/ip.txt')]
   requests_list = []

   for header in headers:
      for ip in ips:
         headerx = {
            header: ip,
            'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text
         }

         requests_list.append(
            grequests.get(url+ "/" +path, headers=headerx)
         )

   requests_list.append(
      grequests.get(url, headers={'X-Original-URL': "/" + path, 'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text})
   )

   requests_list.append(
      grequests.get(url, headers={'X-Rewrite-URL': "/" + path, 'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text})
   )

   responses = grequests.map(requests_list, size=10)

   printresponse(responses)

def portBypass(url):
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)
   print(Fore.CYAN + Style.BRIGHT + "[+] Port Based Bypass" + Style.RESET_ALL)
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)  

   ports = [line.rstrip() for line in open("payload/port.txt")]
   requests_list = []

   for port in ports:
      headerx = {
         'X-Forwarded-Port': port,
         'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text
      }
      
      requests_list.append(
         grequests.get(url, headers=headerx)
      )
   
   responses = grequests.map(requests_list, size=10)

   printresponse(responses)

def HTTPMethodBypass(url):
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)
   print(Fore.CYAN + Style.BRIGHT + "[+] HTTP Method Bypass" + Style.RESET_ALL)
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)  
   
   requests_list = []

   requests_list.append(
      grequests.get(url, headers={'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text})
   )

   requests_list.append(
      grequests.post(url, headers={'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text})
   )

   requests_list.append(
      grequests.put(url, headers={'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text})
   )

   requests_list.append(
      grequests.delete(url, headers={'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text})
   )

   requests_list.append(
      grequests.head(url, headers={'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text})
   )

   requests_list.append(
      grequests.patch(url, headers={'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text})
   )

   responses = grequests.map(requests_list, size=10)

   printresponse(responses)

def ProtocolBypass(url, path):
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)
   print(Fore.CYAN + Style.BRIGHT + "[+] Protocol Based Bypass" + Style.RESET_ALL)
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)

   requests_list = []
   domain = tldextract.extract(url).domain

   url_list = [
      f"http://{domain}/{path}",
      f"https://{domain}/{path}",
   ]

   header_schema = [
      {'X-Forwarded-Scheme': 'http', 'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text},
      {'X-Forwarded-Scheme': 'https', 'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text},
   ]

   for urls in url_list:
      requests_list.append(
         grequests.get(urls, headers={'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text}, verify=False)
      )

   for headerx in header_schema:
      requests_list.append(
         grequests.get(url + "/" + path, headers=headerx)
      )

   responses = grequests.map(requests_list, size=10)

   printresponse(responses)
      
def URLEncodeBypass(url, path):
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)
   print(Fore.CYAN + Style.BRIGHT + "[+]  URL Encode Bypass" + Style.RESET_ALL)
   print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)

   end_urlendcode = [line.rstrip() for line in open("payload/end_urlencode.txt")]
   requests_list = []

   for end in end_urlendcode:
      u = f"{url}/{path}{end}"
      requests_list.append(
         grequests.get(u, headers={'Payloads': u,'User-Agent': ua_generator.generate(device='desktop', browser=('firefox','chrome')).text}, allow_redirects=False, timeout=5)
      )

   responses = grequests.map(requests_list, size=10)

   printresponse(responses)


if __name__ == "__main__":
   if args.header and args.all == False:
      headerBypass(args.url, args.dir)

   if args.protocol and args.all == False:
      ProtocolBypass(args.url, args.dir)

   if args.port and args.all == False:
      portBypass(args.url + "/" + args.dir)

   if args.method and args.all == False:
      HTTPMethodBypass(args.url + "/" + args.dir)

   if args.encode and args.all == False:
      URLEncodeBypass(args.url, args.dir)

   if args.all and args.header == False and args.port == False and args.method == False and args.encode == False and args.protocol == False:
      headerBypass(args.url, args.dir)
      ProtocolBypass(args.url, args.dir)
      portBypass(args.url + "/" + args.dir)
      HTTPMethodBypass(args.url + "/" + args.dir)
      URLEncodeBypass(args.url, args.dir)