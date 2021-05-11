class UnitWord:
    def __init__(self, word: str, interesting: bool, known: bool):
        if type(interesting) != bool:
            raise ValueError('interesting must be bool')
        if type(known) != bool:
            raise ValueError('known must be bool')
        if type(word) != str:
            raise ValueError('word must be bool')
        self.word, self.interesting, self.known = word, interesting, known

class Unit:
    def __init__(self, *words: UnitWord):
        self.words = list(words)

    def ineresting(self):
        return [w.interesting for w in self.words]

    def known(self):
        return [w.known for w in self.words]

    def word(self):
        return [w.word for w in self.words]

    def append(self, word: UnitWord):
        self.words.append(word)

    def __call__(self, n):
        if 0 <= n <= len(self.words):
            return self.words
        raise 'Index out of range'
    
    def __len__(self):
        return len(self.words)

    def __iter__(self):
        return iter(self.words)
