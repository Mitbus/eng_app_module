from os.path import join
from gensim.downloader import base_dir
from gensim.models import Word2Vec
from nltk.corpus import stopwords, words, wordnet
import re


class Word2vec:
    def __init__(self):
        try:
            self.word_dict = set(words.words())
            self.word_synset = wordnet.synsets
            self.stop = set(map(lambda x: x.lower(), stopwords.words('english')))
        except Exception as e:
            from nltk import download
            print(e)
            download('stopwords')
            download('wordnet')
            download('words')
            self.word_dict = set(words.words())
            self.word_synset = wordnet.synsets
            self.stop = set(map(lambda x: x.lower(), stopwords.words('english')))
        try:
            self.model = Word2Vec.load(join(base_dir, 'eng_app_models', 'merged_model'))
        except Exception as e:
            import gensim.downloader as api
            print(e)
            self.model = api.load('word2vec-google-news-300')
        self.incorr_symbols = re.compile(f'[^a-z\'_-]')

    def is_word_correct(self, word):
        return word not in self.stop and self.incorr_symbols.search(word) is None \
        and (len(self.word_synset(word)) != 0 or word in self.word_dict)

    def getSimilarWords(self, vec, maxn, similarity=0.5):
        for (word, sim) in self.model.similar_by_vector(vec, topn=maxn):
            word = word.lower()
            if sim < similarity:
                continue
            if self.is_word_correct(word):
                yield word

    def predict_by_vector(self, vec, maxn=100):
        return (w for w in self.getSimilarWords(vec, maxn))

    def predict_by_word(self, word: str, maxn=100):
        word = word
        if word in self.model.wv:
            vec = self.model.wv[word]
            return self.predict_by_vector(vec, maxn=maxn)
        raise KeyError(f'Word {word} not in vocabulary')

    @property
    def vocab(self):
        if not hasattr(self, '_vocab'):
            self._vocab = [
                w for w in self.model.wv.vocab
                if self.is_word_correct(w)
            ]
        return self._vocab
