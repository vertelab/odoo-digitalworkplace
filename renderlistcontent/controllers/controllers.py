# -*- coding: utf-8 -*-
import json
import urllib.request
from html.parser import HTMLParser

from odoo import http
import logging
_logger = logging.getLogger(__name__)

class MyHTMLParser(HTMLParser):
    found_title = False
    res = ['Error', '', '/renderlistcontent/static/src/img/404PageNotFound.png']
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.found_title = True
        else: 
            self.found_title = False

        if tag == 'meta':
            state = 0
            for a in attrs:
                if 'property' in a[0] and 'title' in a[1]:
                    state = 1
                elif 'property' in a[0] and 'description' in a[1]:
                    state = 2
                elif 'property' in a[0] and 'image' in a[1]:
                    state = 3
                
            for a in attrs:
                if 'content' in a[0] and state == 3 and 'http' in a[1]:
                    self.res[2] = a[1]
                    state = 0
                elif 'content' in a[0] and state > 0 and state != 3:
                    self.res[state - 1] = a[1]
                    state = 0

        elif tag == 'link':
            found = False
            for a in attrs:
                if 'rel' in a[0] and 'icon' in a[1]:
                    found = True

            for a in attrs:
                if found and 'href' in a[0] and 'http' in a[1]:
                    found = False
                    self.res[2] = a[1]

    def handle_data(self, data):
        if self.found_title:
            if data != '':
                self.res[0] = data
            self.found_title = False

class RenderListContent(http.Controller):
    @http.route('/render/<string:url>', auth='public')
    def content(self, url):
        _logger.warning(f"{url}")
        _logger.warning(f"{self}")
        fp = urllib.request.urlopen('https://' + url)
        
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()

        parser = MyHTMLParser()
        parser.found_title = False
        parser.res = ['Error', '', '/renderlistcontent/static/src/img/404PageNotFound.png']
        parser.feed(mystr)
        parser.close()

        if '/renderlistcontent/static/src/img/404PageNotFound.png' in parser.res[2] and not ('Error' in parser.res[0]):
            parser.res[2] = 'https://' + url + '/favicon.ico'
        
        obj = {'res': parser.res}
        tmp = json.dumps(obj)

        return tmp
