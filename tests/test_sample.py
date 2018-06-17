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
import unittest
from functools import partial


class TestAclh(unittest.TestCase):
    
    cmd = [
        'http://www.google.com',
        'http://www.duckduckgo.com',
        'http://en.wikipedia.org',
        '--hdrs', 'User-Agent:Mozilla/5.0'
        ]
    
    def test_get(self):
        aclh = ACLH(self.cmd)
        aclh.start()
    
    def test_print_links(self):
        cmd = self.cmd + ['--print-links', '--no-print']
        aclh = ACLH(cmd)
        aclh.start()
        
if __name__ == '__main__':
    BASEDIR, BASEFILE = os.path.split(os.path.abspath(__file__))
    parent_basedir, __ = os.path.split(BASEDIR)
    sys.path.insert(0, parent_basedir)
    k_dir = os.path.join(parent_basedir, 'aclh')
    sys.path.insert(0, k_dir)
    from aclh import ACLH
    unittest.main()
