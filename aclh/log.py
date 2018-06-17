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

import logging

class Logging:
    
    def __init__(self, name):
        logging.basicConfig(level=logging.ERROR)
        fmt = '%(lineno)s::%(levelname)s::%(module)s::%(funcName)s: %(message)s'
        formatter_ch = logging.Formatter(fmt)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter_ch)
        self.logger = logging.getLogger(name)
        self.logger.addHandler(ch)
        
    def info(self, *args):
        args_list = [str(i) for i in args]
        args_str = '; '.join(args_list)
        self.logger.info(args_str)
        
    def debug(self, *args):
        args_list = [str(i) for i in args]
        args_str = '; '.join(args_list)
        self.logger.debug(args_str)
        
    def warn(self, *args):
        args_list = [str(i) for i in args]
        args_str = '; '.join(args_list)
        self.logger.warn(args_str)
        
    def error(self, *args):
        args_list = [str(i) for i in args]
        args_str = '; '.join(args_list)
        self.logger.error(args_str)
        
    def set_level(self, level):
        level = level.lower()
        if level == 'info':
            self.logger.setLevel(logging.INFO)
        elif level == 'debug':
            self.logger.setLevel(logging.DEBUG)
        elif level in ['warning', 'warn']:
            self.logger.setLevel(logging.WARNING)
        elif level == 'error':
            self.logger.setLevel(logging.ERROR)
        
