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
    return ' '.join([t.strip() for t in text.split('\n') if len(t.strip())])


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
        return '\n'.join([definitions, str(resp.url)])

    @staticmethod
    def parse(resp):
        """ Parse html to retrieve doc
        :returns: @todo

        """
        dom = bs(resp.text).find(id='mainContent')
        print dom.prettify().encode('utf8')
        return
        keyword = dom.find('h2', class_="entryTitle").text
        pronunciation = dom\
            .find('div', class_='entryPronunciation')\
            .find('a')\
            .text
        word_sense = list()
        for sgtag in dom.find_all('section', class_='senseGroup'):
            postag = sgtag.find('h3', class_="partOfSpeech")
            pos = postag.text.strip()
            extra = None
            if postag.next_sibling.name == 'em':
                extra = condense(postag.next_sibling.text)
            defs = list()
            for stag in sgtag.find_all('li', class_='sense'):
                df = condense(stag.find('span', class_='definition').text)
                exs = list()
                for eg_tag in stag.find_all('span', class_='exampleGroup'):
                    eg = []
                    eg_pre = None
                    for em_tag in eg_tag:
                        if em_tag.name == 'em' and \
                                em_tag.has_attr('class') and \
                                'example' in em_tag['class']:
                            eg.append(condense(em_tag.text))
                        else:
                            eg_pre = condense(em_tag.text)
                    exs.append({'ex_title': eg_pre, 'examples': eg})

                defs.append({'definition': df, 'example_groups': exs})
            word_sense.append({'pos': pos,
                               'extra': extra,
                               'defs': defs})
        return {'word': keyword,
                'pronunciation': pronunciation,
                'senses': word_sense}

    @staticmethod
    def format(data):
        """ Format the data from returned
        :returns: @todo

        """
        output = StringIO()
        print >> output, data['word']
        print >> output, data['pronunciation']
        print >> output, ''

        for sg in data['senses']:
            print >> output, '---', sg['pos'].upper(), '---'
            if sg['extra']:
                print >> output, sg['extra']
            for i, s in enumerate(sg['defs']):
                print >> output, '[%d] %s' % (i + 1, s['definition'])
                for eg in s['example_groups']:
                    if eg['ex_title']:
                        print >> output, eg['ex_title']
                    for e in eg['examples']:
                        print >> output, '\t*', e
            print >> output, ''
        return output.getvalue().strip()
