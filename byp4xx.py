import grequests, argparse, os, sys, ua_generator, tldextract, urllib3
from colorama import init, Fore, Style
from pyfiglet import Figlet

def setting_header(headerx):
    set_header = {
        'User-Agent': ua_generator.generate(device='desktop', browser=('firefox', 'chrome')).text,
      #   'Accept-Encoding': urllib3.util.SKIP_HEADER,
      #   'Connection': urllib3.util.SKIP_HEADER,
      #   'Accept': urllib3.util.SKIP_HEADER,
      #   'Content-Length': urllib3.util.SKIP_HEADER,
    }
    headers = {**set_header, **headerx}
    return headers

def initialize_colorama():
    init()

def clear_console():
    os.system("cls||clear")

def display_banner():
    custom_fig = Figlet(font='slant')
    print(Fore.CYAN + Style.BRIGHT + custom_fig.renderText('byp4xx') + Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + "____________________ Rizsyad AR ____________________\n")
    print(Fore.GREEN + Style.BRIGHT + "GREEN\t\t: 2xx Status Code" + Style.RESET_ALL)
    print(Fore.YELLOW + Style.BRIGHT + "YELLOW\t\t: 3xx Status Code" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "RED\t\t: 4xx / 5xx Status Code" + Style.RESET_ALL)
    print("\n")

def create_output_file(results, url):
    domain = tldextract.extract(url).domain
    with open(f"output_{domain}.txt", "a") as file:
        for line in results:
            file.write(line + "\n")

def print_response(url, method, header, status_code, length):
    results = []
    color_map = {
        '2': Fore.GREEN,
        '3': Fore.YELLOW,
        '4': Fore.RED,
    }
    
    status_color = color_map.get(str(status_code)[0], Fore.WHITE)
    colorized_status = f"{status_color}{Style.BRIGHT}{status_code}{Style.RESET_ALL}"
    target_address = f"{method} --> {url}"
    info = f"STATUS: {colorized_status}\tSIZE: {length}"
    info_pure = f"STATUS: {status_code}\tSIZE: {length}"
    remaining = 100 - len(target_address)
    
    print("\n" + target_address + " " * remaining + info)
    print(f"Header= {header}")
    
    results.append("\n" + target_address + " " * remaining + info_pure + f"\nHeader= {header}")
    create_output_file(results, url)

def print_responses(responses):
    for response in responses:
        if response is None:
            continue
        print_response(response.request.url, response.request.method, response.request.headers, response.status_code, response.headers.get('Content-Length'))

def display_banner_title(title):
    print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + f"[+] {title}" + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + "----------------------" + Style.RESET_ALL)

def header_bypass(url, path):
   display_banner_title("HTTP Header Bypass")
    
   headers = [line.rstrip() for line in open("payload/headers.txt")]
   ips = [line.rstrip() for line in open('payload/ip.txt')]
   requests_list = []
    
   for header in headers:
      for ip in ips:
         headerx = {
            header: ip,
         }
            
         requests_list.append(
            grequests.get(url, headers=setting_header(headerx))
         )
    
   requests_list.append(
      grequests.get(url, headers=setting_header({'X-Original-URL': "/" + path}))
   )
    
   requests_list.append(
       grequests.get(url, headers=setting_header({'X-Original-URL': "/" + path}))
   )
    
   responses = grequests.map(requests_list, size=10)
   print_responses(responses)

def port_bypass(url):
   display_banner_title("Port Based Bypass")

   ports = [line.rstrip() for line in open("payload/port.txt")]
   requests_list = []

   for port in ports:
      headerx = {
         'X-Forwarded-Port': port,
      }
      
      requests_list.append(
         grequests.get(url, headers=setting_header(headerx))
      )
   
   responses = grequests.map(requests_list, size=10)

   print_responses(responses)

def method_bypass(url):
   display_banner_title("HTTP Method Bypass")
   
   verbs = [line.rstrip() for line in open("payload/verbs.txt")]
   requests_list = []
   
   for verb in verbs:
      requests_list.append(
         grequests.request(verb, url=url, headers=setting_header({}))
      )

   responses = grequests.map(requests_list, size=10)

   print_responses(responses)

def protocol_bypass(url, path):
   display_banner_title("Protocol Based Bypass")

   requests_list = []
   domain = tldextract.extract(url).domain

   url_list = [
      f"http://{domain}/{path}",
      f"https://{domain}/{path}",
   ]

   header_schema = [
      {'X-Forwarded-Scheme': 'http'},
      {'X-Forwarded-Scheme': 'https'},
   ]

   for urls in url_list:
      requests_list.append(
         grequests.get(urls, headers=setting_header({}), verify=False)
      )

   for headerx in header_schema:
      requests_list.append(
         grequests.get(url + "/" + path, headers=setting_header(headerx))
      )

   responses = grequests.map(requests_list, size=10)

   print_responses(responses)
      
def url_bypass(url, path):
   display_banner_title("URL Encode Bypass")

   end_urlendcode = [line.rstrip() for line in open("payload/end_urlencode.txt")]
   requests_list = []

   for end in end_urlendcode:
      u = f"{url}/{path}{end}"
      requests_list.append(
         grequests.get(u, headers=setting_header({'Payloads': u}), allow_redirects=False, timeout=5)
      )

   responses = grequests.map(requests_list, size=10)

   print_responses(responses)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", "--url", type=str, help="single URL to scan, ex: http://example.com", required=True)
    parser.add_argument("-D", "--dir", type=str, help="Single directory/path to scan, ex: admin", required=True)
    parser.add_argument("-H", '--header', action="store_true", default=False, help="Header Bypass")
    parser.add_argument('-C', "--protocol", action="store_true", default=False, help="Protocol Bypass")
    parser.add_argument("-P", '--port', action="store_true", default=False, help="Port Bypass")
    parser.add_argument("-M", '--method', action="store_true", default=False, help="HTTP Method Bypass")
    parser.add_argument('-E', "--encode", action="store_true", default=False, help="URL Encode Bypass")
    parser.add_argument("-A", '--all', action="store_true", default=False, help="ALL BYPASSES")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    
    print(f"Target: {args.url}\nPath: {args.dir}\n")

    if args.header and not args.all:
        header_bypass(args.url, args.dir)

    if args.protocol and not args.all:
        protocol_bypass(args.url, args.dir)

    if args.port and not args.all:
        port_bypass(args.url + "/" + args.dir)

    if args.method and not args.all:
        method_bypass(args.url + "/" + args.dir)

    if args.encode and not args.all:
        url_bypass(args.url, args.dir)

    if args.all and not any([args.header, args.port, args.method, args.encode, args.protocol]):
      header_bypass(args.url, args.dir)
      protocol_bypass(args.url, args.dir)
      port_bypass(args.url + "/" + args.dir)
      method_bypass(args.url + "/" + args.dir)
      url_bypass(args.url, args.dir)

if __name__ == "__main__":
   clear_console()
   initialize_colorama()
   display_banner()
   main()





