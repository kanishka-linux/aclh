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

if getattr(sys, 'frozen', False):
    BASEDIR, BASEFILE = os.path.split(os.path.abspath(sys.executable))
else:
    BASEDIR, BASEFILE = os.path.split(os.path.abspath(__file__))
    
sys.path.append(BASEDIR)

from vinanti.vinanti import Vinanti
from aclh.aclh import ACLH
from aclh.log import Logging

__version__ = '0.1'
