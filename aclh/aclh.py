"""
Copyright (C) 2018 kanishka-linux kanishka.linux@gmail.com

This file is part of aclh.

aclh is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

aclh is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with aclh.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import time
import argparse
from urllib.parse import urlparse
from vinanti import Vinanti
from log import Logging
from bs4 import BeautifulSoup
from functools import partial

logger = Logging(__name__)

class ACLH:
    
    def __init__(self, args_list):
        self.args_list = args_list
        self.method_list = [
            'get', 'post', 'put','head',
            'patch', 'delete', 'options',
            'crawl'
            ]
        self.parser = argparse.ArgumentParser(
            description='Asynchronous Command-Line HTTP Client'
            )
        self.__add_arguments__()
        
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
        if not no_print and result and result.info:
            print('--Headers--')
            for key, value in result.info.items():
                print('{}: {}'.format(key, value))
            print('-----------')
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

    def start(self, args_list=None):
        if args_list:
            args = self.parser.parse_args(args_list)
        elif self.args_list:
            args = self.parser.parse_args(self.args_list)
        else:
            args = self.parser.parse_args()
        log_level = args.log_level.lower()
        if log_level in ['info', 'debug', 'warning', 'warn', 'error']:
            logger.set_level(log_level)
        logger.debug(self.args_list)
        hdrs_dict, auth_tuple, data_tuple, files_data, proxies, args = self.__process_arguments__(args)
        self.__prepare_request__(hdrs_dict, auth_tuple,
                                 data_tuple, files_data,
                                 proxies, args)
        
    def __add_arguments__(self):
        self.parser.add_argument('urls', metavar='URLS', type=str,
                                 nargs='+', help='list of urls')
        self.parser.add_argument('--url', help='open url', required=False)
        self.parser.add_argument('-i', '--input-files', help='Add urls from files', type=str,
                                 nargs='+', default=None, required=False)
        self.parser.add_argument('--proxy', help='Set Proxy', required=False)
        self.parser.add_argument('--backend', help='set backend, default aiohttp. Available: urllib/aiohttp',
                                 default='aiohttp', required=False)
        self.parser.add_argument('--charset', help='set character set encoding, default utf-8',
                                 default='utf-8', required=False)
        self.parser.add_argument('--log-level', help='set log level', type=str,
                                 default='error', required=False)
        self.parser.add_argument('-o', '--out', help='output file', type=str, nargs='+',
                                 default=None, required=False)
        self.parser.add_argument('-H', '--hdrs', help='Supply HTTP Headers. Format: "key:value"', type=str,
                                 nargs='+', default='User-Agent:Mozilla/5.0',
                                 required=False)
        self.parser.add_argument('-d', '--data', help='Add Data fields. Format: "key:value"', type=str,
                                 nargs='+', default=None, required=False)
        self.parser.add_argument('-f', '--files', help='Add files in POST body', type=str,
                                 nargs='+', default=None, required=False)
        self.parser.add_argument(
            '-X', '--method', default='GET', required=False, type=str,
            help='GET/POST/HEAD/PATCH/PUT/DELETE/OPTIONS/CRAWL'
            )
        self.parser.add_argument('--depth-allowed', help='Set crawling depth. Default 1',
                                 type=int, default=1, required=False)
        self.parser.add_argument('--wait', help='Add wait duration between requests',
                                 type=float, default=0.5, required=False)
        self.parser.add_argument('--timeout', help='Timeout in Seconds',
                                 default=None, required=False)
        self.parser.add_argument('--max-requests', help='Max concurrent requests. Default 10',
                                 type=int, default=10, required=False)
        self.parser.add_argument('--no-print', help='do not print output in terminal',
                                 dest='no_print', default=False, required=False,
                                 action='store_true')
        self.parser.add_argument('--print-links', help='print links in terminal',
                                 default=False, required=False, action='store_true')
        self.parser.add_argument('-c', '--continue', help='Resume download', required=False,
                                 default=False, dest='resume_download', action='store_true')
        self.parser.add_argument('--cookie-unsafe', help='Accept cookies from IP addresses',
                                 required=False, default=False, action='store_true')
        self.parser.add_argument('--binary', help='binary output', required=False,
                                 default=False, action='store_true')
        self.parser.add_argument('--accept-cookies', help='accept session cookies. True/False. Default True',
                                 required=False, default=True, type=bool)
        self.parser.add_argument('--print-cookies', help='show session cookies.',
                                 required=False, default=False, action='store_true')
        self.parser.add_argument('--no-verify', help='do not verify ssl certificate',
                                 required=False, default=False, action='store_true')
        self.parser.add_argument('-u', '--user', help='HTTP Basic Auth. user:passwd',
                                 required=False, default=None)
    
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
                    files_dict.update({file_title:file_name})
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
        logger.debug(data_tuple, files_data)
        return hdrs_dict, auth_tuple, data_tuple, files_data, proxies, args
        
    def __prepare_request__(self, hdrs_dict, auth_tuple,
                            data_tuple, files_data, proxies,
                            args):
        if args.no_verify:
            verify = False
        else:
            verify = True
        logger.debug('verify={}; cookie-unsafe={}'.format(verify, args.cookie_unsafe))
        vnt = Vinanti(block=False, backend=args.backend, hdrs=hdrs_dict,
                      wait=args.wait, max_requests=args.max_requests,
                      continue_out=args.resume_download, verify=verify,
                      auth=auth_tuple, data=data_tuple, cookie_unsafe=args.cookie_unsafe,
                      charset=args.charset, timeout=args.timeout, proxies=proxies,
                      files=files_data, session=args.accept_cookies)
                      
        if args.input_files:
            self.__process_files_urls__(vnt, args)
        else:
            self.__final_request__(vnt, hdrs_dict, auth_tuple,
                                   data_tuple, files_data, proxies,
                                   args)
    
    def __process_files_urls__(self, vnt, args):
        for fl in args.input_files:
            if os.path.isfile(fl):
                logger.debug(fl)
                with open(fl, encoding='utf-8', mode='r') as fd:
                    lines = fd.readlines()
                    logger.debug(lines, 'adding tasks')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('acls '):
                            line = line.replace('acls ', '', 1)
                            line = line.strip()
                        if line:
                            nargs = self.parser.parse_args(line.split())
                            hdrs_d, auth_t, data_t, files_d, prox, nargs = self.__process_arguments__(nargs)
                            self.__final_request__(vnt, hdrs_d, auth_t,
                                                   data_t, files_d, prox,
                                                   nargs)
    
    def __final_request__(self, vnt, hdrs_dict, auth_tuple,
                          data_tuple, files_data, proxies,
                          args):
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
        if args.no_verify:
            verify = False
        else:
            verify = True
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
                func(url[0], onfinished=callback, out=url[1],
                     depth_allowed=depth_allowed, verify=verify,
                     auth=auth_tuple, data=data_tuple, charset=args.charset,
                     timeout=args.timeout, files=files_data)
        else:
            func(args.urls, onfinished=callback, out=args.out,
                 depth_allowed=depth_allowed, verify=verify,
                 auth=auth_tuple, data=data_tuple, charset=args.charset,
                 timeout=args.timeout, files=files_data)
