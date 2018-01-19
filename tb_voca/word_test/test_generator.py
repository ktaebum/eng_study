# -*- coding: utf-8 -*-

import csv
import random

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches
from datetime import datetime

from ..word import Word
from ..helper import print_file_list


class TestGenerator(object):
    def __init__(self, path, section2=True, section3=False):
        """
        :param path: file path
        :param section2: enable section2
        :param section3: enable section3
        """
        word_files = print_file_list(path)
        self.word_list = []
        number = input('File Numbers: ')
        number = list(map(lambda n: int(n), number.split(' ')))
        for n in number:
            try:
                filename = word_files[n - 1]
                self.word_list += self.read_words(filename)
            except IndexError:
                print('Error: Non Existing File Number Included')
        random.shuffle(self.word_list)

        self.answer_doc = None
        self.test_doc = None
        self.question_number = 1
        self.section2 = section2
        self.section3 = section3

    def generate_tests(self):
        """
        section1:  Write meaning for given word (default 50%)
        section2:  Match word for given meaning table set (default 30%)
        section3:  Match word for given sentence (default 20%)
        """

        # Test Preface
        print('There are %d words in total' % (len(self.word_list)))
        num_questions = int(input('Set the number of questions: '))
        if not self.section2 and not self.section3:
            section1_nums = num_questions
            section2_nums = 0
            section3_nums = 0
        else:
            section1_nums = int(input('Number of questions for section 1: '))
            if self.section2:
                section2_nums = int(input('Number of questions for section 2: '))
            else:
                section2_nums = 0
            if self.section3:
                section3_nums = int(input('Number of questions for section 3: '))
            else:
                section3_nums = 0

        assert section1_nums + section2_nums + section3_nums == num_questions, 'Number of questions does not match!'

        print('\n\n')
        print('Test Info')
        print('Total Questions: %d' % num_questions)
        print('Section1: %d' % section1_nums)
        print('Section2: %d' % section2_nums)
        print('Section3: %d' % section3_nums)
        print('\n\n')

        if self.section3:
            section3 = random.sample(list(filter(lambda word: word.sentence != '', self.word_list)), k=section3_nums)
            if len(section3) < section3_nums:
                section1_nums += section3_nums - len(section3)
            map(lambda word: self.word_list.remove(word), section3)
            section3 = list(map(lambda word: word.remove_word_from_sentence(), section3))
        else:
            section3 = []
        section1 = self.word_list[:section1_nums]
        section2 = self.word_list[section1_nums:section1_nums + section2_nums]

        self.answer_doc = Document()
        self.test_doc = Document()

        answer_sections = self.answer_doc.sections
        test_sections = self.test_doc.sections
        for answer_section, test_section in zip(answer_sections, test_sections):
            answer_section.top_margin = Inches(0.5)
            answer_section.bottom_margin = Inches(0.5)
            test_section.top_margin = Inches(0.5)
            test_section.bottom_margin = Inches(0.5)

        # Basic Font Setting
        answer_font = self.answer_doc.styles['Normal'].font
        test_font = self.test_doc.styles['Normal'].font
        answer_font.name = 'Times New Roman'
        answer_font.size = Pt(9)
        test_font.name = 'Times New Roman'
        test_font.size = Pt(10)
        test_day = datetime.now()

        answer_header = self.answer_doc.add_paragraph()
        answer_header.style = self.answer_doc.styles['Heading 2']
        answer_header.add_run('Answer')
        answer_header.add_run(
            text='\t\t\t\t\t\t\t\t\t%d-%d-%d' % (test_day.year, test_day.month, test_day.day + 1))

        test_header = self.test_doc.add_paragraph()
        test_header.style = self.test_doc.styles['Heading 2']
        test_header.add_run('Test')
        test_header.add_run(
            text='\t\t\t\t\t\t\t\t\t\t%d-%d-%d' % (test_day.year, test_day.month, test_day.day + 1)
        ).alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        self.make_section1(section1)
        self.make_section2(section2)
        self.make_section3(section3)

        self.answer_doc.save('answer.docx')
        self.test_doc.save('test.docx')

        return

    def make_section1(self, section1):
        answer = self.answer_doc.add_paragraph()
        test = self.test_doc.add_paragraph()
        answer.add_run('Answer for section 1').bold = True
        test.add_run('Section 1: Write ').bold = True
        meaning = test.add_run('meaning')
        meaning.bold = True
        meaning.italic = True
        test.add_run(' and at least one ').bold = True
        synonym = test.add_run('synonym')
        synonym.bold = True
        synonym.italic = True
        test.add_run(' of given words').bold = True
        # test.add_run('Section 1: Write meaning and at least one synonym of given words').bold = True

        for word in section1:
            self.answer_doc.add_paragraph('%d) %s / %s' % (self.question_number, word.e_mean, word.k_mean))
            self.test_doc.add_paragraph('%d) %s' % (self.question_number, word.word))
            self.question_number += 1

        return

    def make_section2(self, section2):
        if len(section2) == 0:
            return
        answer = self.answer_doc.add_paragraph()
        test = self.test_doc.add_paragraph()
        answer.add_run('Answer for section 2').bold = True
        test.add_run('Section 2: Match word for given meaning').bold = True

        self.test_doc.add_paragraph('============================================================================')
        word_index = ord('a')
        p = None
        for i, word in enumerate(section2):
            word.set_index(chr(word_index))
            if i % 5 == 0:
                p = self.test_doc.add_paragraph()
            p.add_run('(%s) %s \t' % (word.index, word))
            word_index += 1

        random.shuffle(section2)

        self.test_doc.add_paragraph('============================================================================')
        for word in section2:
            self.test_doc.add_paragraph('%d) %s / %s' % (self.question_number, word.e_mean, word.k_mean))
            self.answer_doc.add_paragraph('%d) (%s)-%s' % (self.question_number, word.index, word.word))
            self.question_number += 1

        return

    def make_section3(self, section3):
        if len(section3) == 0:
            return
        answer = self.answer_doc.add_paragraph()
        test = self.test_doc.add_paragraph()
        answer.add_run('Answer for section 3').bold = True
        test.add_run('Section 3: Select ').bold = True
        appropriate = test.add_run('the most appropriate')
        appropriate.bold = True
        appropriate.italic = True
        test.add_run(' word for given sentence from following choices').bold = True
        choices = ['a', 'b', 'c', 'd']
        for word in section3:
            self.test_doc.add_paragraph('%d) %s' % (self.question_number, word.sentence))
            answer_choice = random.choice(choices)
            choice = self.test_doc.add_paragraph('')
            for c in choices:
                if c == answer_choice:
                    choice.add_run('(%s) %s\t' % (c, word.word))
                    self.answer_doc.add_paragraph('%d) (%s)-%s' % (self.question_number, c, word.word))
                    word.choice_appear += 1
                else:
                    other = random.choice(section3)
                    while other.choice_appear == 4 or other == word:
                        other = random.choice(section3)
                    choice.add_run('(%s) %s\t' % (c, other.word))
                    other.choice_appear += 1

            self.question_number += 1

        return

    @staticmethod
    def read_words(filename):
        """
        :param filename:  target file name (include related path)
                            target csv file must follow word, e_mean, k_mean, sentence order!
        :return: word list
        """

        file = open('{:s}'.format(filename), 'r', encoding='utf-8')

        reader = csv.reader(file)
        words = []
        for line in reader:
            words.append(Word(word=line[0],
                              e_mean=line[1],
                              k_mean=line[2],
                              sentence=line[3]))
        file.close()

        return words
