# -*- coding: utf-8 -*-
"""
A Crawler for 沪江小D - http://dict.hjenglish.com/jp/
沪江小D is a online Japanese-Chinese dictionary.
By Charles Ouyang
2016.06.24
"""
import urllib2
import bs4

# request header
req_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, sdch', # compressed data, not needed here
    'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2,ja;q=0.2',
    'Connection': 'close',
    'Referer': None
}


class Word:
    """
    Basic unit of a dictionary
    """

    def __init__(self, _japanese):
        """
        init method
        :param _japanese:
        """
        # Japanese word
        self.japanese = _japanese
        # Japanese kana
        self.kana = None
        # romaji for Japanese word
        self.romaji = None
        # word property
        self.property = None
        # Chinese meaning
        self.chinese = None

        self.translate()

    def __str__(self):
        """
        to string
        :return:
        """
        string = ''
        string += 'japanese: ' + self.japanese + '\n'
        string += 'kana: ' + self.kana + '\n'
        string += 'romaji: ' + self.romaji + '\n'
        string += 'property: ' + self.property + '\n'
        string += 'chinese: ' + self.chinese + '\n'
        return string.encode('utf8')

    def translate(self):
        """
        get info from website
        :return:
        """
        url = 'http://dict.hjenglish.com/jp/jc/' + self.japanese
        request = urllib2.Request(url, None, req_header)
        # if messy code
        # content = content.decode('unicode-escape')
        content = urllib2.urlopen(request).read()
        soup = bs4.BeautifulSoup(content, 'html.parser')

        if soup is None:
            return

        soup_word = soup.find(id='headword_jp_1')
        self.japanese = soup_word.find(id='jpword_1').string
        self.kana = soup_word.find_all(class_='trs_jp')[0].string[1:-1]
        self.romaji = soup_word.find_all(class_='trs_jp')[1].string[1:-1]

        # there are two kind of structures, one of which could be missing
        if len(soup_word.find_all(class_='simple_content')) != 0:
            self.property = soup_word.find_all(class_='simple_content')[0].find('b').string[1:-1]
            self.chinese = soup_word.find_all(class_='simple_content')[0].contents[2]
        elif len(soup_word.find_all(class_='tip_content_item')) != 0:
            self.property = soup_word.find_all(class_='tip_content_item')[0].string[1:-2]
            self.chinese = soup_word.find_all(class_='soundmark_color')[0].string

        # examples TBD

        return soup_word
