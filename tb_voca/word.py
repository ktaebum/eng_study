class Word(object):
    def __init__(self, word, e_mean='', k_mean='', sentence=''):
        self.word = word
        self.e_mean = e_mean
        self.k_mean = k_mean
        self.sentence = sentence.replace(word, '_____')
        self.index = ''

    def __str__(self):
        return self.word

    def set_index(self, index):
        self.index = index
