class Word(object):
    def __init__(self, word, e_mean='', k_mean='', sentence=''):
        self.word = word
        self.e_mean = e_mean
        self.k_mean = k_mean
        self.sentence = sentence
        self.index = ''
        self.choice_appear = 0
        self.appeared = False

    def __str__(self):
        return self.word

    def set_index(self, index):
        self.index = index

    def equal(self, word):
        if type(word) != type(self):
            return False
        return self.word == word.word and \
               self.e_mean == word.e_mean and \
               self.k_mean == word.k_mean and \
               self.sentence == word.sentence

    def remove_word_from_sentence(self):
        self.sentence = self.sentence.replace(self.word, '______')
        return self
