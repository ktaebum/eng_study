# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from ..word import Word
from os import listdir
from os.path import isfile, join
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
        word_files = [file for file in listdir(path) if isfile(join(path, file))]
        print('Select Target File Number to Generate Test')
        for i in range(len(word_files)):
            print('  ㄴ', (i + 1), word_files[i])

        try:
            number = int(input('Number: ')) - 1
        except FileNotFoundError:
            print('Error: Non Existing File!')
            return

        self.filename = word_files[number]
        self.word_list = []

        file = open('./find_targets/{:s}'.format(self.filename), 'r', encoding='utf-8')
        reader = csv.reader(file)
        for line in reader:
            self.word_list.append(Word(word=line[0]))
        file.close()

        return

    def find(self):
        new_file_name = self.filename.split('.csv')[0] + '_result.csv'
        file = open('./find_targets/{:s}'.format(new_file_name), 'w', encoding='utf-8', newline='')
        wr = csv.writer(file)
        for word in self.word_list:
            eng_mean, kor_mean, example = WordFinder.find_single_word(word.word)
            word.e_mean = ''
            for e_mean in eng_mean:
                word.e_mean += e_mean
                word.e_mean += ',  '
            word.k_mean = ''
            for k_mean in kor_mean:
                word.k_mean += k_mean
                word.k_mean += ',  '
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
        print('Finding \'%s\'...' % (word))
        eng_results = soup.find('ul', {'class': 'semb'}).find_all('div', {'class': 'trg'})
        eng_meanings = list(map(lambda list_element: WordFinder.tag_parser(
            str(list_element.find('span', {'class': 'ind'}))), eng_results))
        eng_meanings = list(filter(lambda mean: len(mean) > 0, eng_meanings))

        example = soup.find('div', {'class': 'ex'})
        if not example:
            example = 'not founded'
        else:
            example = WordFinder.tag_parser(str(example.find('em')))

        # now find korean meanings
        req = requests.get(WordFinder.kor_url + word)
        soup = BeautifulSoup(req.text, 'html.parser')
        kor_meanings = soup.find('ul', {'class': 'list_search'}).find_all('li')
        kor_meanings = list(map(lambda list_element: WordFinder.tag_parser(
            str(list_element.find('span', {'class': 'txt_search'}).find('daum:word'))), kor_meanings))

        if len(eng_meanings) == 0:
            eng_meanings = 'not founded'
        if len(kor_meanings) == 0:
            kor_meanings = 'not founded'

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
