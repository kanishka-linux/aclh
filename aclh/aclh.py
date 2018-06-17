import os
import sys
import time
import argparse
from urllib.parse import urlparse
from vinanti import Vinanti
from bs4 import BeautifulSoup
from functools import partial

class ACLH:
    
    def __init__(self, args_list):
        self.args_list = args_list
        self.method_list = [
            'get', 'post', 'put','head',
            'patch', 'delete', 'options',
            'crawl'
            ]

    def __get_page__(self, *args):
        result = args[-1]
        url = args[-2]
        sr = args[-3]
        no_print = args[0]
        print_lnk = args[1]
        ytm = args[2]
        vnt = args[3]
        cookies = args[4]
        sys.stdout.write('\r')
        sys.stdout.flush()
        if result and result.html:
            soup = None
            if not no_print: 
                soup = BeautifulSoup(result.html, 'html.parser')
                print(soup.prettify())
            if print_lnk:
                if soup is None:
                    soup = BeautifulSoup(result.html, 'html.parser')
                for link in soup.find_all('a'):
                    lnk = link.get('href')
                    txt = link.text
                    print(lnk, txt)
            print('{} {} {} {} {}s'
                  .format(
                    result.status, result.content_type, sr,
                    url, round(time.time() - ytm, 2)
                    )
                  )
            if cookies:
                print('Cookie: {}'.format(result.session_cookies))
            print(vnt.tasks_count(), vnt.tasks_done(), vnt.tasks_remaining())

    def start(self):
        args = self.__add_arguments__(self.args_list)
        self.__process_arguments__(args)
    
    def __add_arguments__(self, args_list):
        parser = argparse.ArgumentParser(description='Asynchronous Command-Line HTTP Client')
        
        parser.add_argument('urls', metavar='URLS', type=str,
                            nargs='+', help='list of urls')
        parser.add_argument('--url', help='open url', required=False)
        parser.add_argument('--proxy', help='Set Proxy', required=False)
        parser.add_argument('--backend', help='set backend, default aiohttp',
                            default='aiohttp', required=False)
        parser.add_argument('--charset', help='set character set encoding, default utf-8',
                            default='utf-8', required=False)
        parser.add_argument('-o', '--out', help='output file', type=str, nargs='+',
                            default=None, required=False)
        parser.add_argument('-H', '--hdrs', help='Supply HTTP Headers', type=str,
                            nargs='+', default='User-Agent:Mozilla/5.0',
                            required=False)
        parser.add_argument('-d', '--data', help='Add Data fields', type=str,
                            nargs='+', default=None, required=False)
        parser.add_argument('-f', '--files', help='Add files in POST body', type=str,
                            nargs='+', default=None, required=False)
        parser.add_argument('-X', '--method', help='Type of HTTP request', type=str,
                            default='GET', required=False)
        parser.add_argument('--depth-allowed', help='Set crawling depth. Default 1',
                            type=int, default=1, required=False)
        parser.add_argument('--wait', help='Add wait duration between requests',
                            type=float, default=0.5, required=False)
        parser.add_argument('--timeout', help='Timeout in Seconds',
                            default=None, required=False)
        parser.add_argument('--max-requests', help='Max concurrent requests. Default 10',
                            type=int, default=10, required=False)
        parser.add_argument('--no-print', help='do not print output in terminal',
                            dest='no_print', default=False, required=False,
                            action='store_true')
        parser.add_argument('--print-links', help='print links in terminal',
                            default=False, required=False, action='store_true')
        parser.add_argument('-c', '--continue', help='Resume download', required=False,
                            default=False, dest='resume_download', action='store_true')
        parser.add_argument('--cookie-unsafe', help='Accept cookies from IP addresses',
                            required=False, default=False, action='store_true')
        parser.add_argument('--binary', help='binary output', required=False,
                            default=False, action='store_true')
        parser.add_argument('--accept-cookies', help='accept session cookies. True/False. Default True',
                            required=False, default=True, action='store_true')
        parser.add_argument('--print-cookies', help='show session cookies.',
                            required=False, default=False, action='store_true')
        parser.add_argument('--verify', help='ssl certificate verification',
                            required=False, default=True, action='store_true')
        parser.add_argument('-u', '--user', help='HTTP Basic Auth. user:passwd',
                            required=False, default=None)
        if args_list is None:
            args = parser.parse_args()
        else:
            args = parser.parse_args(args_list)
        return args
    
    def __process_arguments__(self, args):
        hdrs = args.hdrs
        hdrs_dict = {}
        if isinstance(hdrs, str):
            key, val = hdrs.split(':')
            hdrs_dict.update({key.strip():val.strip()})
        elif isinstance(hdrs, list):
            for hdr in hdrs:
                key, val = hdr.split(':')
                hdrs_dict.update({key.strip():val.strip()})
        wait = args.wait
        max_requests = args.max_requests
        continue_out = args.resume_download
        if args.user:
            user, passwd = args.user.split(':')
            auth_tuple = (user, passwd)
        else:
            auth_tuple = None
        data_list = []
        data_tuple = None
        if args.data:
            for i in args.data:
                key, val = i.split(':')
                data_list.append((key, val))
            data_tuple = tuple(data_list)
        
        files_list = []
        files_dict = {}
        files_data = None
        if args.files:
            for i in args.files:
                if '@' in i:
                    file_title, file_name = i.split('@')
                    files_dict.update({file_title, file_name})
                else:
                    files_list.append(i)
            if files_dict:
                files_data = files_dict
            else:
                files_data = tuple(files_list)
        
        if args.proxy:
            proxy_type = urlparse(args.proxy).scheme
            proxies = {proxy_type:args.proxy}
        else:
            proxies = None
        vnt = Vinanti(block=False, backend=args.backend, hdrs=hdrs_dict, wait=wait,
                      max_requests=max_requests, continue_out=continue_out,
                      verify=args.verify, auth=auth_tuple, data=data_tuple,
                      cookie_unsafe=args.cookie_unsafe, charset=args.charset,
                      timeout=args.timeout, proxies=proxies, files=files_data,
                      session=args.accept_cookies)
        method = args.method.lower()
        
        if method in self.method_list:
            func = eval('vnt.{}'.format(method))
        else:
            func = vnt.get
            
        ytm = time.time()
        depth_allowed = args.depth_allowed
        callback = partial(self.__get_page__, args.no_print,
                           args.print_links, ytm, vnt,
                           args.print_cookies)
        if args.out:
            out_list = []
            if len(args.out) == len(args.urls):
                out_list = [i for i in args.out]
            elif len(args.out) == 1:
                if args.out[0] == 'default':
                    out_list = ['default' for i in args.urls]
                elif os.path.isdir(args.out[0]):
                    out_list = [args.out[0] for i in args.urls]
            for url in zip(args.urls, out_list):
                func(url[0], onfinished=callback,
                     out=url[1], depth_allowed=depth_allowed)
        else:
            func(args.urls, onfinished=callback,
                 out=args.out, depth_allowed=depth_allowed)
