# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from ..word import Word
from ..helper import print_file_list
import requests
import re
import csv


class WordFinder(object):
    eng_url = 'https://en.oxforddictionaries.com/definition/'  # use Oxford Dictionary
    kor_url = 'http://alldic.daum.net/search.do?q='  # use Daum dictionary for korean meaning

    def __init__(self, path):
        """
        :param path: path for word files (upper directory)
        """
        print('Select Target File Number to Generate Test')
        word_files = print_file_list(path)
        number = int(input('Number: ')) - 1
        if number >= len(word_files):
            raise FileNotFoundError('Non-Existing File!')

        self.filename = word_files[number]

        self.word_list = []

        file = open('{:s}'.format(self.filename), 'r', encoding='utf-8')
        reader = csv.reader(file)
        for line in reader:
            self.word_list.append(Word(word=line[0]))
        file.close()

        return

    def find(self):
        # find target words in csv file and save it into new file
        new_file_name = './find_results/' + (self.filename.split('/')[-1]).split('.csv')[0] + '_result.csv'
        file = open('{:s}'.format(new_file_name), 'w', encoding='utf-8', newline='')
        wr = csv.writer(file)
        for word in self.word_list:
            eng_mean, kor_mean, example = WordFinder.find_single_word(word.word)
            word.e_mean = ''
            for i, e_mean in enumerate(eng_mean):
                word.e_mean += '%d. %s, ' % (i + 1, e_mean)
            word.k_mean = ''
            for i, k_mean in enumerate(kor_mean):
                word.k_mean += '%d. %s, ' % (i + 1, k_mean)
            word.sentence = example
            wr.writerow([word.word, word.e_mean, word.k_mean, word.sentence])
        file.close()

    @staticmethod
    def find_single_word(word):
        """
        :param word: target word
        Just find the most representative meaning, and following example sentence
        return (english_meaning as list, korean_meaning as list, example as string)
        """

        # first, find english meaning and following example
        req = requests.get(WordFinder.eng_url + word)
        soup = BeautifulSoup(req.text, 'html.parser')
        print('Finding \'%s\'...' % word)

        eng_results = soup.find('ul', {'class': 'semb'}).find_all('div', {'class': 'trg'})

        try:
            eng_meanings = list(map(lambda list_element: WordFinder.tag_parser(
                str(list_element.find('span', {'class': 'ind'}))), eng_results))
            eng_meanings = list(filter(lambda mean: len(mean) > 0, eng_meanings))
        except AttributeError:
            eng_meanings = ['']

        try:
            example = WordFinder.tag_parser(str(soup.find('div', {'class': 'ex'}).find('em')))
        except AttributeError:
            example = ''

        # now find korean meanings
        req = requests.get(WordFinder.kor_url + word)
        soup = BeautifulSoup(req.text, 'html.parser')

        try:
            kor_meanings = soup.find('ul', {'class': 'list_search'}).find_all('li')
            kor_meanings = list(map(lambda list_element: WordFinder.tag_parser(
                str(list_element.find('span', {'class': 'txt_search'}).find('daum:word'))), kor_meanings))
        except AttributeError:
            kor_meanings = ['']

        return eng_meanings, kor_meanings, example

    @staticmethod
    def tag_parser(string):
        """
        remove <something> </something> in html tag
        :param string: input tag string
        :return: just content of the tag
        """
        searcher = re.search('>(.*)<', string)
        if searcher:
            return searcher.group(1)
        else:
            return ''
