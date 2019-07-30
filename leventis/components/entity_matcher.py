from spacy.gold import spans_from_biluo_tags
from leventis.tags import Tags, BiGramTags


class EntityMatcher(object):

    name = 'entity_matcher'

    def __init__(self, model):
        self.model = model
        self.features = model._features()

    def __call__(self, doc):
        features = self.features.doc_to_features(doc)
        predicted_tags = self.model.predict(features)
        biluo_tags = self.predicted_to_bilou(predicted_tags)
        doc.ents = spans_from_biluo_tags(doc, biluo_tags)
        return doc

    def predicted_to_bilou(self, predicted_tags):
        tags = self.get_tags(predicted_tags)
        return tags.to_bilou()

    def get_tags(self, predicted_tags):
        return Tags(predicted_tags)


class BiGramEntityMatcher(EntityMatcher):

    name = 'bigram_entity_matcher'

    def get_tags(self, predicted_tags):
        return BiGramTags(predicted_tags)
