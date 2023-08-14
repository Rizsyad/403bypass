# 403bypass

[![GitHub issues](https://img.shields.io/github/issues/rizsyad/403bypass)](https://github.com/rizsyad/403bypass/issues)
[![GitHub forks](https://img.shields.io/github/forks/rizsyad/403bypass)](https://github.com/rizsyad/403bypass/network)
[![GitHub stars](https://img.shields.io/github/stars/rizsyad/403bypass)](https://github.com/rizsyad/403bypass/stargazers)
[![GitHub license](https://img.shields.io/github/license/rizsyad/403bypass)](https://github.com/rizsyad/403bypass)

## Introduction

This is the tool that I wrote when I was working for pentest. 

## Usage 

To display help message use the -h flag:

```bash
$ python3 byp4xx.py -h
```
```
    __                __ __           
   / /_  __  ______  / // / _  ___  __
  / __ \/ / / / __ \/ // /_| |/_/ |/_/
 / /_/ / /_/ / /_/ /__  __/>  <_>  <  
/_.___/\__, / .___/  /_/ /_/|_/_/|_|  
      /____/_/                        

____________________ Rizsyad AR ____________________

GREEN           : 2xx Status Code
YELLOW          : 3xx Status Code
RED             : 4xx Status Code
MAGENTA         : 5xx Status Code


usage: byp4xx.py [-h] --url URL -D DIR [-H] [-C] [-P] [-M] [-E] [-A]

optional arguments:
  -h, --help         show this help message and exit
  --url URL, ---urlrl URL  single URL to scan, ex: http://example.com
  -D DIR, --dir DIR  Single directory/path to scan, ex: admin
  -H, --header       Header Bypass
  -C, --protocol     Protocol Bypass
  -P, --port         Port Bypass
  -M, --method       HTTP Method Bypass
  -E, --encode       URL Encode Bypass
  -A, --all          ALL BYPASSES
```
## How To Run

- Scan with specific payloads:
  * [ `-H` / `--header` ] Support HEADER based bypasses/payloads
    ```bash
    root@root:$ python byp4xx.py --url https://target.com --dir secret --header
    ```
  * [ `-C` / `--protocol` ] Support PROTOCOL based bypasses/payloads
    ```bash
    root@root:$ python byp4xx.py --url https://target.com --dir secret --protocol
    ```
  * [ `-P` / `--port` ] Support PORT based bypasses/payloads
    ```bash
    root@root:$ python byp4xx.py --url https://target.com --dir secret --port
    ```
  * [ `-M` / `--method` ] Support HTTP Method based bypasses/payloads
    ```bash
    root@root:$ python byp4xx.py --url https://target.com --dir secret --method
    ```
  * [ `-E` / `--encode` ] Support URL Encoded bypasses/payloads
    ```bash
    root@root:$ python byp4xx.py --url https://target.com --dir secret --encode
    ```
  * [ `-A` / `--all` ] All bypasses/payloads
    ```bash
    root@root:$ python byp4xx.py --url https://target.com --dir secret --all
    ```

## Installation

- git clone https://github.com/Rizsyad/403bypass.git
- cd 403bypass
- pip3 install -r requirements.txt

## Features
- Bypass using HTTP Verbs(GET , HEAD , POST , PUT , DELETE , PATCH)
- Bypass using payloads
- Bypass using headers
- Bypass using port