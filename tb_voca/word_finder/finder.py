# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from ..word_io import print_file_list, read_csv
import requests
import re
import csv


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


class WordFinder(object):
    eng_url = 'https://en.oxforddictionaries.com/definition/'  # use Oxford Dictionary
    kor_url = 'http://alldic.daum.net/search.do?q='  # use Daum dictionary for korean meaning

    def __init__(self, path, all_files=False):
        """
        :param path: path for word files (upper directory)
        """
        if not all_files:
            print('Select Target File Number to Find')
            word_files = print_file_list(path, verbose=True)
            number = int(input('Number: ')) - 1
            if number >= len(word_files):
                raise FileNotFoundError('Non-Existing File!')

            self.filename = word_files[number]

            self.word_list = read_csv(self.filename)
        else:
            # If all files is True, find all csv file in target path
            word_files = print_file_list(path, verbose=False)
            for file in word_files:
                self.filename = file
                self.word_list = read_csv(self.filename)
                self.find()

        return

    def find(self):
        # find target words in csv file and save it into new file
        new_file_name = './find_results/' + (self.filename.split('/')[-1]).split('.csv')[0] + '_result.csv'
        file = open('{:s}'.format(new_file_name), 'w', encoding='utf-8', newline='')
        wr = csv.writer(file)
        for word in self.word_list:
            print('Finding \'%s\'...' % word)
            if word.e_mean == '':
                eng_mean = WordFinder.find_eng_meaning(word.word)
                for i, e_mean in enumerate(eng_mean):
                    word.e_mean += '%d. %s, ' % (i + 1, e_mean)

            if word.k_mean == '':
                kor_mean = WordFinder.find_kor_meaning(word.word)
                for i, k_mean in enumerate(kor_mean):
                    word.k_mean += '%d. %s, ' % (i + 1, k_mean)

            if word.sentence == '':
                word.sentence = WordFinder.find_example(word.word)
            wr.writerow([word.word, word.e_mean, word.k_mean, word.sentence])
        file.close()

    @staticmethod
    def find_example(word):
        """
        :param word: input word
        :return:
        """
        req = requests.get(WordFinder.eng_url + word)
        soup = BeautifulSoup(req.text, 'html.parser')
        try:
            example = tag_parser(str(soup.find('div', {'class': 'ex'}).find('em')))
        except AttributeError:
            example = ''
        return example

    @staticmethod
    def find_eng_meaning(word):
        """
        :param word: input word
        :return:
        """
        req = requests.get(WordFinder.eng_url + word)
        soup = BeautifulSoup(req.text, 'html.parser')
        eng_results = soup.find('ul', {'class': 'semb'}).find_all('div', {'class': 'trg'})

        try:
            eng_meanings = list(map(lambda list_element: tag_parser(
                str(list_element.find('span', {'class': 'ind'}))), eng_results))
            eng_meanings = list(filter(lambda mean: len(mean) > 0, eng_meanings))
        except AttributeError:
            eng_meanings = ['']

        return eng_meanings

    @staticmethod
    def find_kor_meaning(word):
        """
        :param word: input word
        :return:
        """
        # now find korean meanings
        req = requests.get(WordFinder.kor_url + word)
        soup = BeautifulSoup(req.text, 'html.parser')

        try:
            kor_meanings = soup.find('ul', {'class': 'list_search'}).find_all('li')
            kor_meanings = list(map(lambda list_element: tag_parser(
                str(list_element.find('span', {'class': 'txt_search'}).find('daum:word'))), kor_meanings))
        except AttributeError:
            kor_meanings = ['']

        return kor_meanings

    @staticmethod
    def find_single_word(word):
        """
        :param word: target word
        Just find the most representative meaning, and following example sentence
        return (english_meaning as list, korean_meaning as list, example as string)
        """
        return WordFinder.find_eng_meaning(word), WordFinder.find_kor_meaning(word), WordFinder.find_example(word)
