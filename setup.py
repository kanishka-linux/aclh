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


import platform
from setuptools import setup

"""
 GNU/Linux users should install dependencies manually using their native
 package manager
"""


setup(
    name='aclh',
    version='0.1',
    license='GPLv3',
    author='kanishka-linux',
    author_email='kanishka.linux@gmail.com',
    url='https://github.com/kanishka-linux/aclh',
    long_description="README.md",
    packages=['aclh', 'aclh.vinanti'],
    include_package_data=True,
    install_requires = ['bs4', 'aiohttp'],
    description="Asynchronous command line HTTP client",
    entry_points={
        'console_scripts':['aclh = aclh.__main__:main']
        }, 
)
