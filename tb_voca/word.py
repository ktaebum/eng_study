class Word(object):
    def __init__(self, word, e_mean='', k_mean='', sentence=''):
        self.word = word
        self.e_mean = e_mean
        self.k_mean = k_mean
        self.sentence = sentence
        self.index = ''
        self.choice_appear = 0

    def __str__(self):
        return self.word

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.word == other.word and \
               self.e_mean == other.e_mean and \
               self.k_mean == other.k_mean and \
               self.sentence == other.sentence

    def __ne__(self, other):
        return not self.__eq__(other)

    def __copy__(self):
        word = Word(word=self.word,
                    e_mean=self.e_mean,
                    k_mean=self.k_mean,
                    sentence=self.sentence)
        word.index = self.index
        word.choice_appear = self.choice_appear
        return word

    def set_index(self, index):
        self.index = index

    def remove_word_from_sentence(self):
        # For preventing some defensive programming issue, make new Word instance
        return Word(word=self.word,
                    e_mean=self.e_mean,
                    k_mean=self.k_mean,
                    sentence=self.sentence.replace(self.word, '______'))
