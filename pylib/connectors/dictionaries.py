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
from bs4 import BeautifulSoup as bs
from bs4.element import Comment
import subprocess as sp


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
        dom = bs(resp.text)
        tag = dom.find(class_='entryPageContent')
        if not tag:
            tag = dom.find(class_='responsive_cell_center')
            return unicode(tag)
        links = list(tag.findAll('a'))
        [c.decompose() for c in tag.find_all(lambda t: t is Comment)]

        for a in links:
            if a.string and ('ore example' not in a.string)\
                    and ('View synonyms' not in a.string):
                em = dom.new_tag('em')
                s = dom.new_string(a.string)
                em.append(s)
                a.replace_with(em)
            else:
                a.decompose()
        try:
            tag.find(class_='sound').decompose()
        except AttributeError:
            pass
        try:
            tag.find('div', class_='etymology').decompose()
        except AttributeError:
            pass
        return unicode(tag)

    @staticmethod
    def format(page):
        """ Format the page

        :page: @todo
        :returns: @todo

        """
        pandoc = sp.Popen(['pandoc', '-f', 'html', '-t', 'markdown_github'],
                          stdin=sp.PIPE, stdout=sp.PIPE)
        pandoc.stdin.write(page.encode('utf-8'))
        pandoc.stdin.close()
        return pandoc.stdout.read()
