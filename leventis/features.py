import nltk
from abc import ABC, abstractmethod
from nltk.corpus import wordnet

from leventis.helpers import is_abbreviated_form


class Features(ABC):

    def doc_to_features(self, doc):
        tokens = self.tokenise_doc(doc)
        return self.to_features(tokens)

    def to_features(self, tokens):
        return [self.extract_features(tokens, i) for i in range(len(tokens))]

    @abstractmethod
    def tokenise_doc(self, doc):
        pass

    @staticmethod
    @abstractmethod
    def extract_features(tokens, index):
        pass


class WordFeatures(Features):

    name = 'WordFeatures'

    def tokenise_doc(self, doc):
        # Extract the docs parts we need for the features
        return [token.text for token in doc]

    @staticmethod
    def extract_features(tokens, index):
        word = tokens[index]
        features = {
            'bias': 1.0,
            'spelling': 1 if wordnet.synsets(word) else 0,
            'word[-4:]': word[-4:],
            'word[-3:]': word[-3:],
            'word[-2:]': word[-2:],
            'is_abbreviated': is_abbreviated_form(word),
            'capitalised_first_letter': word[0].isupper(),
        }
        return features


class BiGramFeatures(Features):

    name = 'BiGramFeatures'

    def tokenise_doc(self, doc):
        # Extract the docs parts we need for the features
        return list(nltk.bigrams([t.text for t in doc]))

    def to_features(self, bigrams):
        return [self.extract_features(bigram) for bigram in bigrams]

    @staticmethod
    def extract_features(bigram):

        features = {
            'word-0_upper_first_char': bigram[0][0].isupper(),
            'word-1_lower': bigram[1].islower(),
            'word-1_alpha': bigram[1].replace('-', '').isalpha(),
            'word-1_lower_first_char': bigram[1][0].islower(),
        }

        if is_abbreviated_form(bigram[0]):
            features['word-0-abbreviated'] = True
        else:
            features['word-0-alpha'] = bigram[0].isalpha()
            features['word-0-title'] = len(bigram[0]
                                           ) > 2 and bigram[0].istitle()

        for index, word in enumerate(bigram):

            features[f'word-{index}'] = word
            features[f'word-{index}_spelling'] = 1 if wordnet.synsets(
                word) else 0

            for x in range(3, 5):
                if len(word) >= x:
                    features[f'word-{index}_suffix-{x}'] = word[-x:]

        return features
