# aclh

**A**synchronous **C**ommand-**l**ine **H**TTP Client

## Features

+ Supports Asynchronous HTTP requests from command-line.

+ Can handle 100 or even 1000+ HTTP requests asynchronously in a single thread (Thanks to aiohttp).

+ Ability to resume partial downloads.

+ Ability to accept input from files containing urls with custom parameters.

+ Automatic HTML Formatting, in order to make reading of HTML content easier inside terminal (Thanks to bs4).

+ Allows adjusting maximum number of concurrent requests.

+ Allows adjusting time duration between successive requests to same domain.

+ Supports two backends urllib and aiohttp for fetching urls. 

+ Built-in lightweight crawler

## Why to use aclh?

If users want to fire just one request at a time from cli then there is no need to use **aclh**, since existing clients like curl or wget are sufficient for this. But, if users are interested in firing 100+ or more concurrent requests asynchronously without creating 100+ or more separate processes, then they might find **aclh** useful.


## Dependencies and Installation
    
### Dependencies

        python 3.5.2+
        
        aiohttp
        
        bs4

### Installation
        
        $ git clone https://github.com/kanishka-linux/aclh
        
        $ cd aclh
        
        $ python setup.py sdist (or python3 setup.py sdist)
        
        $ cd dist
        
        $ (sudo) pip install pkg_available_in_directory (or pip3 install pkg_available_in_directory) 
        
          # where 'pkg_available_in_directory' is the exact name of the package
          
          # created in the 'dist' folder
          
        
        # OR
        
        
        $ (sudo) pip install git+https://github.com/kanishka-linux/aclh.git
        
**Note:** use 'sudo' depending on whether you want to install package system-wide or not
        
**Note:** use pip or pip3 depending on what is available on your system

### Uninstall
        
        $ (sudo) pip uninstall aclh (OR pip3 uninstall aclh)

## Brief Documentation:

1. Fetch three urls and print their formatted HTML output in terminal

        $ aclh https://en.wikipedia.org https://mr.wikipedia.org https://www.duckduckgo.com

2. Fetch Two urls asynchronously and save their output in two separate files

        $ aclh https://en.wikipedia.org https://mr.wikipedia.org --out en.html mr.html
        
3. Fetch Two urls asynchronously and save their output in a directory with default names.

        $ aclh https://en.wikipedia.org https://mr.wikipedia.org --out=/tmp
        
4. Fetch Two urls asynchronously, do not print output on terminal but print cookies and links within pages.

        $ aclh https://en.wikipedia.org https://mr.wikipedia.org --no-print --print-cookies --print-links
        
5. Fetch urls with options from files

        $ aclh --input-files file1.txt file2.txt
        
6. Send common Custom header when fetching two urls

        $ aclh https://en.wikipedia.org https://www.python.org/ --hdrs 'User-Agent:Mozilla/5.0' 'Cookie: custom_cookie'
        
7. Crawl website asynchronously and keep time duration of 1s between successive requests

        $ aclh -X CRAWL 'https://docs.python.org/3/' --depth-allowed=1 --wait=1.0
        
8. help

        $ aclh -h

## How does it achieve async?

Using [Vinanti](https://github.com/kanishka-linux/vinanti) and [aiohttp](https://github.com/aio-libs/aiohttp). All the heavy lifting is done by these two libraries. **aclh** provides cli wrapper around them.

## Note: 

Currently aclh is a beta level software.
