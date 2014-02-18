#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: dictionaries.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:
    A set of connectior to online dictionaries.


"""


from StringIO import StringIO
import requests
from bs4 import BeautifulSoup as BS
from html2text import html2text
import re

ITALIANENV = re.compile(r'_\s*([^_]*)\s*_')
COLONSPACE = re.compile(r':\s*')
ORDINAL = re.compile(r'\b([0-9]+)')


class Connector(object):

    """ Connectors will be used for connecting to online dictionaries
        querying for keywords and return a Markdown formated resource.
    """

    def __init__(self, base_url):
        """ The base_url is an endpoint

        :base_url: @todo

        """
        self._base_url = base_url

    def get_page(self, **kwargs):
        """ Query the online source

        :**kwargs:
        :returns: @todo

        """
        return requests.get(self._base_url, params=kwargs)


def condense(text):
    """ remove extra whitespaces between words, e.g., spaces and newline

    :text: @todo
    :returns: @todo

    """
    return '\n'.join([t.strip() for t in text.split('\n') if len(t.strip())])


class OxfordDictionaries(Connector):

    """ Connecting to Oxford Dictionary online"""

    def __init__(self):
        """@todo: to be defined1.

        :base_url: @todo

        """
        Connector.__init__(self,
                           'http://oxforddictionaries.com/search/english/')
        self._default_kwargs = {'direct': 1, 'multi': 1}

    def query(self, keywords):
        """ Querying keywords

        :keywords: @todo
        :returns: @todo

        """
        q = {'q': keywords}
        q.update(self._default_kwargs)
        resp = self.get_page(**q)
        resp.encoding = 'UTF-8'
        definitions = OxfordDictionaries.format(OxfordDictionaries.parse(resp))
        return condense(definitions)

    @staticmethod
    def parse(resp):
        """ Parse html to retrieve doc
        :returns: @todo

        """
        dom = BS(resp.text).find(class_='entryPageContent')
        children = dom.children
        children.next()
        content_tag = children.next()
        #import pudb; pudb.set_trace()
        for a in dom.findAll('a'):
            a.decompose()
        txt = html2text(str(dom).decode('utf-8'))
        return txt

    @staticmethod
    def format(data):
        """ Format the data from returned.
        :returns: @todo

        """
        data = '\n'.join([l.strip() for l in data.split('\n') if len(l)])
        data = ITALIANENV.sub(r'_\1_', data)
        data = COLONSPACE.sub(r': ', data)
        data = ORDINAL.sub(r'\1 ', data)
        return data
